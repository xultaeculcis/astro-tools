<img src="docs/assets/logo.png" alt="" width="300" style="float: right" align="right" />

# astro-tools

Astrophotography tools for managing data assets and running automated image processing.

It supports ZIP validation, renaming, directory creation, and uploads to cloud storage. Image processing features are currently under development.

## ✨ Features

- **ZIP Integrity Check**
    Quickly validate downloaded archives (fast listing or full test).

- **Telescope.Live ZIP Renaming**
    Normalize filenames using metadata to pattern:
    `<TARGET>_<TELESCOPE>_<FILTERS>_<FRAMES>[-<OBS_NUM>].zip`

- **Directory Creation**
    Bulk-create target directories from a plain text list.

- **Cloud Uploads**
    Upload datasets from local disk or Google Drive to Azure Blob Storage.

- **🔭 Image Processing (WIP / TODO)**
    Workflows for stacking, calibrating, and enhancing astro images are under active development.

## 📦 Installation

### For Usage

Requires **Python 3.12+**

```bash
pip install git+https://github.com/xultaeculcis/astro-tools.git
```

### For Development

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and set up
git clone https://github.com/xultaeculcis/astro-tools.git
cd astro-tools
uv sync

# Configure environment
mv .env-sample .env
# Fill in .env with your secrets
```

## 🚀 CLI Examples

### Check ZIP files

```bash
astro-tools zip check \
  --directory=/path/to/zips \
  --log_file=check.log \
  --workers=10 \
  --fast
```

### Rename ZIPs

```bash
astro-tools rename-zips --data_dir=/path/to/zips
```

### Create Target Directories

```bash
astro-tools create-dirs \
  --names_fp=./data/names.txt \
  --target_dir=/path/to/target
```

### Upload to Blob Storage

```bash
astro-tools blob upload \
  --source_dir=/path/to/zips \
  --container=datasets \
  --prefix=telescope-live/raw-zips
```

## ☁️ GDrive to Azure (via Colab)

Use in Google Colab to upload shared data directly:

```python
from google.colab import drive
drive.mount('/content/drive')
```

```bash
pip install git+https://github.com/xultaeculcis/astro-tools.git
astro-tools blob upload \
  --source_dir=/content/drive/MyDrive/Shared/Astrophoto_Release \
  --container=datasets \
  --prefix=whwang/gdrive-export
```

## 🛠️ License

MIT © [xultaeculcis](https://github.com/xultaeculcis/astro-tools/blob/main/LICENSE)
