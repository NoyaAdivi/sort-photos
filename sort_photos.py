"""
sort_photos.py - Sort a large photo collection into "documents" vs "photos"
using a zero-shot CLIP model. Runs fully offline after the first model download,
CPU-only friendly (old laptops are fine, just slower).

Output folders (inside --dst):
    documents/   - photographed documents, receipts, screenshots, notes, IDs...
    photos/      - real photos (people, family, places, food, etc.)
    uncertain/   - the model wasn't confident enough -> check these by hand

The original folder structure is preserved under each output folder, so files
with the same name never overwrite each other.

Usage examples (Windows):
    python sort_photos.py "D:\\Pictures" "D:\\Sorted" --dry-run --limit 300
    python sort_photos.py "D:\\Pictures" "D:\\Sorted"
    python sort_photos.py "D:\\Pictures" "D:\\Sorted" --move

It is safe to stop (Ctrl+C) and run again: already-processed files are skipped
(tracked in results.csv inside --dst).
"""

import argparse
import csv
import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# ---------------------------------------------------------------------------
# Prompts: each category is a list of text descriptions. A picture's score for
# a category is the sum of the probabilities of its prompts.
# Feel free to add/remove prompts if you see systematic mistakes.
# ---------------------------------------------------------------------------
CATEGORIES = {
    "documents": [
        "a photo of a document",
        "a photo of a printed page with text",
        "a photo of a receipt",
        "a photo of an invoice or a bill",
        "a photo of a form",
        "a photo of a handwritten note",
        "a photo of an ID card",
        "a photo of a whiteboard with writing",
        "a screenshot of a phone or computer screen",
        "a photo of a page from a book",
    ],
    "photos": [
        "a photo of people",
        "a family photo",
        "a selfie",
        "a photo of a child",
        "a group photo at an event",
        "a photo of a landscape",
        "a photo of a city street",
        "a photo of food",
        "a photo of an animal",
        "a photo of a room or a house",
    ],
}

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff", ".gif", ".heic", ".heif"}

MODEL_NAME = "ViT-B-32"               # light model, good for CPU
MODEL_WEIGHTS = "laion2b_s34b_b79k"


def parse_args():
    p = argparse.ArgumentParser(description="Sort photos into documents / photos / uncertain using CLIP.")
    p.add_argument("src", help="Folder with the images (scanned recursively)")
    p.add_argument("dst", help="Output folder (must NOT be inside src)")
    p.add_argument("--move", action="store_true", help="Move files instead of copying (default: copy)")
    p.add_argument("--dry-run", action="store_true", help="Only classify and write results.csv, don't copy/move")
    p.add_argument("--threshold", type=float, default=0.75,
                   help="Minimum confidence for a decision; below it -> uncertain (default 0.75)")
    p.add_argument("--batch-size", type=int, default=32, help="Images per batch (default 32)")
    p.add_argument("--no-quantize", action="store_true",
                   help="Disable int8 speed-up (use only if you get errors or bad results)")
    p.add_argument("--workers", type=int, default=0,
                   help="Threads for loading images (default: number of CPU cores)")
    p.add_argument("--threads", type=int, default=0, help="CPU threads for torch (default: all cores)")
    p.add_argument("--limit", type=int, default=0, help="Process only the first N new images (for testing)")
    return p.parse_args()


def find_images(src: Path, dst: Path):
    dst_resolved = dst.resolve()
    for root, dirs, files in os.walk(src):
        root_path = Path(root)
        # never descend into the output folder
        dirs[:] = [d for d in dirs if (root_path / d).resolve() != dst_resolved]
        for f in files:
            if Path(f).suffix.lower() in IMAGE_EXTS:
                yield root_path / f


def load_done(csv_path: Path):
    done = set()
    if csv_path.exists():
        with open(csv_path, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                done.add(row["source"])
    return done


def unique_target(target: Path) -> Path:
    if not target.exists():
        return target
    stem, suffix, i = target.stem, target.suffix, 1
    while True:
        candidate = target.with_name(f"{stem}_{i}{suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def main():
    args = parse_args()
    src = Path(args.src)
    dst = Path(args.dst)

    if not src.is_dir():
        sys.exit(f"Source folder not found: {src}")
    if dst.resolve() == src.resolve():
        sys.exit("dst must be different from src")
    dst.mkdir(parents=True, exist_ok=True)

    # Heavy imports after argument checks so --help is fast
    import torch
    import open_clip
    from PIL import Image, ImageOps
    from tqdm import tqdm

    try:
        from pillow_heif import register_heif_opener
        register_heif_opener()
    except ImportError:
        pass  # HEIC files will just fail to open and be marked as errors

    Image.MAX_IMAGE_PIXELS = None  # allow very large scans

    if args.threads > 0:
        torch.set_num_threads(args.threads)

    csv_path = dst / "results.csv"
    done = load_done(csv_path)

    print("Scanning for images...")
    all_images = [p for p in find_images(src, dst) if str(p) not in done]
    if args.limit > 0:
        all_images = all_images[: args.limit]
    print(f"{len(done)} already processed, {len(all_images)} to process.")
    if not all_images:
        return

    print(f"Loading model {MODEL_NAME} (first run downloads ~600MB)...")
    model, _, preprocess = open_clip.create_model_and_transforms(MODEL_NAME, pretrained=MODEL_WEIGHTS)
    tokenizer = open_clip.get_tokenizer(MODEL_NAME)
    model.eval()

    # Pre-compute text embeddings once
    prompts, prompt_cat = [], []
    for cat, plist in CATEGORIES.items():
        for t in plist:
            prompts.append(t)
            prompt_cat.append(cat)
    cat_names = list(CATEGORIES.keys())
    cat_index = torch.tensor([cat_names.index(c) for c in prompt_cat])

    with torch.inference_mode():
        text_feat = model.encode_text(tokenizer(prompts))
        text_feat = text_feat / text_feat.norm(dim=-1, keepdim=True)

    # Speed-up 1: int8 quantization of the image model's linear layers.
    # ViT is mostly linear layers, so this is typically ~1.5-2x faster on CPU.
    if not args.no_quantize:
        try:
            model.visual = torch.ao.quantization.quantize_dynamic(
                model.visual, {torch.nn.Linear}, dtype=torch.qint8)
            print("int8 speed-up enabled")
        except Exception as e:
            print(f"int8 speed-up not available on this machine ({e}); continuing without it")

    def load(path: Path):
        try:
            with Image.open(path) as im:
                # Speed-up 2: decode JPEGs directly at ~1/8 size (CLIP only needs 224px).
                # Must be called before anything else touches the pixels.
                im.draft("RGB", (224, 224))
                im = ImageOps.exif_transpose(im)   # respect phone rotation
                im = im.convert("RGB")
                return preprocess(im)
        except Exception as e:  # corrupt / unsupported file
            return e

    new_file = not csv_path.exists()
    csv_fh = open(csv_path, "a", newline="", encoding="utf-8")
    writer = csv.writer(csv_fh)
    if new_file:
        writer.writerow(["source", "category", "confidence", "documents_score", "photos_score", "target"])

    counts = {**{c: 0 for c in cat_names}, "uncertain": 0, "error": 0}
    workers = args.workers or (os.cpu_count() or 4)
    pool = ThreadPoolExecutor(max_workers=workers)
    batches = [all_images[i: i + args.batch_size] for i in range(0, len(all_images), args.batch_size)]

    def submit(batch):
        return [pool.submit(load, p) for p in batch]

    try:
        with tqdm(total=len(all_images), unit="img") as bar:
            # Speed-up 3: load the NEXT batch from disk while the model works on this one.
            next_futures = submit(batches[0])
            for b_idx, batch_paths in enumerate(batches):
                loaded = [f.result() for f in next_futures]
                if b_idx + 1 < len(batches):
                    next_futures = submit(batches[b_idx + 1])

                good_paths, tensors = [], []
                for pth, item in zip(batch_paths, loaded):
                    if isinstance(item, Exception):
                        writer.writerow([str(pth), "error", "", "", "", str(item)[:200]])
                        counts["error"] += 1
                    else:
                        good_paths.append(pth)
                        tensors.append(item)

                if tensors:
                    with torch.inference_mode():
                        img_feat = model.encode_image(torch.stack(tensors))
                        img_feat = img_feat / img_feat.norm(dim=-1, keepdim=True)
                        probs = (100.0 * img_feat @ text_feat.T).softmax(dim=-1)
                        cat_scores = torch.zeros(len(tensors), len(cat_names))
                        cat_scores.index_add_(1, cat_index, probs)

                    for pth, scores in zip(good_paths, cat_scores):
                        conf, idx = scores.max(dim=0)
                        conf = float(conf)
                        category = cat_names[int(idx)] if conf >= args.threshold else "uncertain"
                        counts[category] += 1

                        target_str = ""
                        if not args.dry_run:
                            rel = pth.relative_to(src)
                            target = unique_target(dst / category / rel)
                            target.parent.mkdir(parents=True, exist_ok=True)
                            if args.move:
                                shutil.move(str(pth), str(target))
                            else:
                                shutil.copy2(str(pth), str(target))
                            target_str = str(target)

                        writer.writerow([
                            str(pth), category, f"{conf:.3f}",
                            f"{float(scores[cat_names.index('documents')]):.3f}",
                            f"{float(scores[cat_names.index('photos')]):.3f}",
                            target_str,
                        ])

                csv_fh.flush()
                bar.update(len(batch_paths))
    except KeyboardInterrupt:
        print("\nStopped. Run the same command again to continue where you left off.")
    finally:
        pool.shutdown(wait=False, cancel_futures=True)
        csv_fh.close()

    print("\nDone this run:", ", ".join(f"{k}: {v}" for k, v in counts.items()))
    print(f"Full log: {csv_path}")


if __name__ == "__main__":
    main()
