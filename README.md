# sort-photos

Sort a large photo collection into **documents** (photographed papers, receipts, screenshots, notes, IDs) and **photos** (people, family, places, food, etc.) using a zero-shot [CLIP](https://github.com/mlfoundations/open_clip) model.

- **No training and no labeling needed.** The model compares each image to short text descriptions.
- **Runs fully offline** after the first model download, so your photos never leave your computer.
- **CPU-friendly.** It works on old laptops, with int8 quantization and fast JPEG decoding.
- **Safe by default.** It copies files and does not move them, and the original folder is untouched.
- **Resumable.** Stop it with Ctrl+C and run the same command again to continue.

## How it works

Each image is scored against two groups of text prompts, for example `"a photo of a receipt"` or `"a family photo"`. The group with the highest total probability wins.

If the confidence is below a threshold (0.75 by default), the image goes to `uncertain/` so you can review it by hand.

## Installation

Requires Python 3.9+.

```bash
pip install -r requirements.txt
```

`requirements.txt` installs the CPU-only build of PyTorch, which is much smaller than the GPU build. If you have an NVIDIA GPU, install PyTorch from [pytorch.org](https://pytorch.org/get-started/locally/) first.

## Usage

Do a dry run on 300 images first. This classifies the images and writes `results.csv`, but copies nothing:

```bash
python sort_photos.py "D:\Pictures" "D:\Sorted" --dry-run --limit 300
```

Open `D:\Sorted\results.csv` to check the results. Then delete it and run on everything:

```bash
python sort_photos.py "D:\Pictures" "D:\Sorted"
```

The output folder must not be inside the source folder.

### Output

```
Sorted/
├── documents/    # original sub-folder structure is preserved
├── photos/
├── uncertain/    # low-confidence images; review these manually
└── results.csv   # one row per image: category, confidence, scores, target path
```

Corrupt or unreadable files are logged as `error` in `results.csv` and are not copied.

### Options

| Option | Description |
| --- | --- |
| `--dry-run` | Classify only and write `results.csv`; don't copy or move anything |
| `--limit N` | Process only the first N new images |
| `--threshold X` | Minimum confidence for a decision (default `0.75`). Lower it to get fewer `uncertain` images |
| `--move` | Move files instead of copying them |
| `--batch-size N` | Images per batch (default `32`). Lower it if you run out of memory |
| `--no-quantize` | Disable the int8 speed-up |
| `--workers N` | Threads used for loading images (default: number of CPU cores) |
| `--threads N` | CPU threads used by PyTorch (default: all cores) |

## Improving accuracy

Edit the `CATEGORIES` dictionary at the top of `sort_photos.py`. If a certain kind of image keeps being misclassified, add a prompt that describes it to the right group, for example `"a photo of a medical prescription"` under `documents`.

You can also add a new group, such as `"screenshots"`, and it will get its own output folder automatically.

## Performance

Speed depends on your CPU. The progress bar shows images per second. On an older 2–4 core laptop, expect roughly 30–90 minutes for 40,000 images. Run a dry run with `--limit 300` to see the speed on your machine.

The first run downloads the model, which is about 600 MB.

## Supported formats

JPG, PNG, BMP, WEBP, TIFF, GIF and HEIC/HEIF. HEIC support comes from the `pillow-heif` package.
