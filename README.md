# X2GIF

Download Twitter/X GIFs as real `.gif` files directly.

## Install

Make sure you have **Python 3.8+** and [ffmpeg](https://ffmpeg.org/) installed.

Installing directly from this repo:
```bash
pip install git+https://github.com/SNINMNON/x2gif.git
```

Installing ffmpeg:
- **Windows** → `winget install "FFmpeg (Essentials Build)"` and add to PATH.
- **macOS** → `brew install ffmpeg`
- **Linux** → `sudo apt install ffmpeg` (or equivalent for distro).

## Usage

```bash
x2gif https://x.com/user/status/1234567890
```

To remove background:
```bash
x2gif https://x.com/user/status/1234567890 -r
```

All option args
```bash
x2gif [-h] [--fps FPS] [--width WIDTH] [-o OUTPUT] [-r] [--color COLOR] [--similarity SIMILARITY] [--blend BLEND] url
```