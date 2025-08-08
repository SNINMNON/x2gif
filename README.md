# X2GIF

Download Twitter/X GIFs as real `.gif` files directly.

## Install

Make sure you have **Python 3.9+** and [ffmpeg](https://ffmpeg.org/) installed.

Installing dependencies:
```bash
pip install x2gif
```

Installing ffmpeg:
- **Windows** → `winget install "FFmpeg (Essentials Build)"` and add to PATH.
- **macOS** → `brew install ffmpeg`
- **Linux** → `sudo apt install ffmpeg` (or equivalent for distro).

## Usage

```bash
python x2gif.py "https://x.com/user/status/1234567890"
```

To remove background:

```bash
python gif.py "https://x.com/user/status/1234567890" -r
```

Check all option args:
```bash
python gif.py -h
```