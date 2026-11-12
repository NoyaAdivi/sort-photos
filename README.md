<p align="center">
  <a href="https://github.com/NoyaAdivi/sort-photos"><img src="docs/readme/banner-en.svg" width="100%" alt="Sort Photos: an offline AI photo classifier"></a>
</p>

<p align="center"><a href="README.he.md"><img src="docs/readme/lang-he.svg" height="44" alt="לגרסה בעברית"></a></p>

<p align="center">
  <a href="#quick-start"><img src="https://img.shields.io/badge/Quick_start-FFD5C9?style=for-the-badge&logo=rocket&logoColor=A8483A" alt="Quick start"></a>
  <a href="#how-it-works"><img src="https://img.shields.io/badge/How_it_works-DAD5FF?style=for-the-badge&logo=pytorch&logoColor=5548C8" alt="How it works"></a>
  <a href="sort_photos.py"><img src="https://img.shields.io/badge/View_the_code-D9F3E7?style=for-the-badge&logo=python&logoColor=1F7350" alt="View the code"></a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/NoyaAdivi/sort-photos?color=DAD5FF&labelColor=5548C8" alt="License"></a>
  <a href="https://github.com/NoyaAdivi/sort-photos/commits/main"><img src="https://img.shields.io/github/last-commit/NoyaAdivi/sort-photos?color=FFD5C9&labelColor=A8483A" alt="Last commit"></a>
  <a href="https://github.com/NoyaAdivi/sort-photos"><img src="https://img.shields.io/github/languages/top/NoyaAdivi/sort-photos?color=D9F3E7&labelColor=1F7350" alt="Top language"></a>
  <a href="https://github.com/NoyaAdivi/sort-photos"><img src="https://img.shields.io/github/repo-size/NoyaAdivi/sort-photos?color=FBD5E0&labelColor=A03A5C" alt="Repo size"></a>
</p>

<h3 align="center">Separate your documents from your memories, without labeling a single photo.</h3>

<p align="center">
  Sort Photos goes through a big photo collection and splits it into <b>documents</b> (receipts, papers, screenshots, notes, IDs)<br>and <b>photos</b> (people, family, places, food) with a zero-shot <a href="https://github.com/mlfoundations/open_clip">CLIP</a> model.
</p>

<table align="center">
  <tr>
    <td align="center" width="25%"><a href="#how-it-works"><b>🧠 0</b></a><br><sub>labels or training</sub></td>
    <td align="center" width="25%"><a href="#highlights"><b>🔒 100%</b></a><br><sub>offline, private</sub></td>
    <td align="center" width="25%"><a href="#output"><b>📁 3</b></a><br><sub>output folders</sub></td>
    <td align="center" width="25%"><a href="#formats"><b>🖼️ 7</b></a><br><sub>image formats</sub></td>
  </tr>
</table>

<a name="highlights"></a>
<p align="center"><a href="#highlights"><img src="docs/readme/highlights-en.svg" width="100%" alt="Highlights"></a></p>

<table>
  <tr valign="top">
    <td width="33%"><p><b>🧠 Smart without training</b></p><ul><li><b>Zero-shot:</b> each image is compared to short text prompts</li><li><b>Confidence threshold:</b> unsure images go to <code>uncertain/</code></li><li><b>Easy to extend:</b> add a prompt or a whole new folder</li></ul></td>
    <td width="33%"><p><b>🔒 Safe for your photos</b></p><ul><li><b>Runs offline</b> after the first model download</li><li><b>Copies, never moves</b> by default; the source stays untouched</li><li><b>Resumable:</b> stop with Ctrl+C and run again to continue</li></ul></td>
    <td width="33%"><p><b>⚡ Fast on old laptops</b></p><ul><li><b>int8 quantization</b> for about 1.5-2x speed on CPU</li><li><b>Fast JPEG decoding</b> and multi-threaded loading</li><li><b>Dry run</b> on a sample to check results and speed</li></ul></td>
  </tr>
</table>

<a name="how-it-works"></a>
<p align="center"><a href="#how-it-works"><img src="docs/readme/how-it-works-en.svg" width="100%" alt="How it works"></a></p>

```mermaid
flowchart LR
  A([📂 Your photo folder]) --> B[Load and resize<br/>multi-threaded]
  B --> C[CLIP ViT-B-32<br/>image embedding]
  P([Text prompts<br/>'a photo of a receipt'<br/>'a family photo']) --> C
  C --> D{Confidence<br/>≥ 0.75?}
  D -->|yes| E([📄 documents/])
  D -->|yes| F([🖼️ photos/])
  D -->|no| G([🤔 uncertain/])
  C --> R([📊 results.csv])
  style A fill:#E8E4FF,stroke:#6F60F0,color:#2C2668
  style P fill:#FFE6DE,stroke:#E36E57,color:#2C2668
  style E fill:#D9F3E7,stroke:#1F7350,color:#1F4D38
  style F fill:#D9F3E7,stroke:#1F7350,color:#1F4D38
  style G fill:#FFF1C9,stroke:#B98A1E,color:#5C4410
  style R fill:#DAD5FF,stroke:#5548C8,color:#2C2668
```

Each image is scored against two groups of text prompts. The group with the highest total probability wins. Below the threshold (0.75 by default), the image goes to <code>uncertain/</code> for a quick manual check.

<a name="output"></a>
<details open>
<summary><b>📁 Output</b></summary>

```
Sorted/
├── documents/    original sub-folder structure is kept
├── photos/
├── uncertain/    low-confidence images, review these by hand
└── results.csv   one row per image: category, confidence, scores, target path
```
Corrupt or unreadable files are logged as <code>error</code> in <code>results.csv</code> and are not copied.
</details>

<a name="tech-stack"></a>
<p align="center"><a href="#tech-stack"><img src="docs/readme/tech-stack-en.svg" width="100%" alt="Tech Stack"></a></p>

<p align="center">
  <a href="https://www.python.org"><img src="https://img.shields.io/badge/Python-CFE6FA?style=for-the-badge&logo=python&logoColor=3F6D9F" alt="Python"></a>
  <a href="https://pytorch.org"><img src="https://img.shields.io/badge/PyTorch-FBD5E0?style=for-the-badge&logo=pytorch&logoColor=A03A5C" alt="PyTorch"></a>
  <a href="https://github.com/mlfoundations/open_clip"><img src="https://img.shields.io/badge/OpenCLIP-DAD5FF?style=for-the-badge&logo=openai&logoColor=5548C8" alt="OpenCLIP"></a>
  <a href="https://python-pillow.org"><img src="https://img.shields.io/badge/Pillow-D9F3E7?style=for-the-badge&logo=python&logoColor=1F7350" alt="Pillow"></a>
  <a href="https://pandas.pydata.org"><img src="https://img.shields.io/badge/pandas-FFD5C9?style=for-the-badge&logo=pandas&logoColor=A8483A" alt="pandas"></a>
</p>

<a name="quick-start"></a>
<p align="center"><a href="#quick-start"><img src="docs/readme/quick-start-en.svg" width="100%" alt="Quick start"></a></p>

Requires **Python 3.9+**. [`requirements.txt`](requirements.txt) installs the small CPU-only build of PyTorch. With an NVIDIA GPU, install PyTorch from [pytorch.org](https://pytorch.org/get-started/locally/) first.

```bash
pip install -r requirements.txt
```

1. **Dry run on 300 images** (classifies and writes `results.csv`, copies nothing):
   ```bash
   python sort_photos.py "D:\Pictures" "D:\Sorted" --dry-run --limit 300
   ```
2. **Check** `D:\Sorted\results.csv`, then delete it.
3. **Sort everything:**
   ```bash
   python sort_photos.py "D:\Pictures" "D:\Sorted"
   ```

> [!NOTE]
> The output folder must not be inside the source folder. The first run downloads the model (about 600 MB).

<details>
<summary><b>⚙️ All options</b></summary>

| Option | Description |
| --- | --- |
| `--dry-run` | Classify only and write `results.csv`; don't copy or move anything |
| `--limit N` | Process only the first N new images |
| `--threshold X` | Minimum confidence for a decision (default `0.75`) |
| `--move` | Move files instead of copying them |
| `--batch-size N` | Images per batch (default `32`); lower it if memory runs out |
| `--no-quantize` | Disable the int8 speed-up |
| `--workers N` | Threads for loading images (default: CPU cores) |
| `--threads N` | CPU threads for PyTorch (default: all cores) |
</details>

<details>
<summary><b>🎯 Improving accuracy</b></summary>

Edit the `CATEGORIES` dictionary at the top of [`sort_photos.py`](sort_photos.py). If a kind of image keeps landing in the wrong place, add a prompt that describes it to the right group, for example `"a photo of a medical prescription"` under `documents`. A new group, such as `"screenshots"`, gets its own output folder automatically.
</details>

<a name="formats"></a>
<details>
<summary><b>🖼️ Formats and speed</b></summary>

JPG, PNG, BMP, WEBP, TIFF, GIF and HEIC/HEIF (through `pillow-heif`). On an older 2-4 core laptop, expect roughly 30-90 minutes for 40,000 images; the progress bar shows images per second.
</details>

<a name="contact"></a>
<p align="center"><a href="#contact"><img src="docs/readme/footer-en.svg" width="100%" alt="Built by Noya Adivi"></a></p>

<p align="center">
  <a href="https://github.com/NoyaAdivi/sort-photos"><img src="https://img.shields.io/badge/Open_project-FFD5C9?style=for-the-badge&logo=github&logoColor=A8483A" alt="Open project"></a>
  <a href="https://www.linkedin.com/in/noya-adivi/"><img src="https://img.shields.io/badge/LinkedIn-DAD5FF?style=for-the-badge&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzU1NDhDOCIgZD0iTTIwLjQ1IDIwLjQ1aC0zLjU2di01LjU3YzAtMS4zMy0uMDMtMy4wNC0xLjg1LTMuMDQtMS44NiAwLTIuMTQgMS40NS0yLjE0IDIuOTR2NS42N0g5LjM1VjloMy40MXYxLjU2aC4wNWMuNDgtLjkgMS42NC0xLjg1IDMuMzctMS44NSAzLjYgMCA0LjI3IDIuMzcgNC4yNyA1LjQ2djYuMjh6TTUuMzQgNy40M2EyLjA2IDIuMDYgMCAxIDEgMC00LjEzIDIuMDYgMi4wNiAwIDAgMSAwIDQuMTN6TTcuMTIgMjAuNDVIMy41NlY5aDMuNTZ2MTEuNDV6TTIyLjIyIDBIMS43N0MuNzkgMCAwIC43NyAwIDEuNzN2MjAuNTRDMCAyMy4yMy43OSAyNCAxLjc3IDI0aDIwLjQ1Yy45OCAwIDEuNzgtLjc3IDEuNzgtMS43M1YxLjczQzI0IC43NyAyMy4yIDAgMjIuMjIgMHoiLz48L3N2Zz4=" alt="LinkedIn"></a>
  <a href="https://noyaadivi.github.io/noya-website"><img src="https://img.shields.io/badge/Portfolio-D9F3E7?style=for-the-badge&logo=githubpages&logoColor=1F7350" alt="Portfolio"></a>
  <a href="https://github.com/NoyaAdivi"><img src="https://img.shields.io/badge/More_projects-FBD5E0?style=for-the-badge&logo=github&logoColor=A03A5C" alt="More projects"></a>
</p>
