import argparse, os, re, subprocess, sys, tempfile
import cv2
from yt_dlp import YoutubeDL
from datetime import datetime

def _hex_to_ffmpeg(color: str) -> str:
    """Convert '#fff'/'#ffffff'/'ffffff' -> '0xFFFFFF' for ffmpeg colorkey."""
    s = color.strip().lstrip('#')
    if len(s) == 3:
        s = ''.join(ch * 2 for ch in s)
    if not re.fullmatch(r'[0-9a-fA-F]{6}', s):
        raise ValueError(f"Invalid hex color: {color}")
    return '0x' + s.upper()

def dl_video(tweet_url, outdir):
    ydl_opts = {
        "outtmpl": os.path.join(outdir, "%(id)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "merge_output_format": "mp4",
        "format": "mp4/best"
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(tweet_url, download=True)
        path = ydl.prepare_filename(info)
        base, ext = os.path.splitext(path)
        return base + ".mp4" if not ext.lower().endswith("mp4") and os.path.exists(base + ".mp4") else path

def mp4_to_gif(mp4_path, gif_path, fps=None, width=None,
               remove_bg=False, bg_color="#ffffff", similarity=0.10, blend=0.00):
    if fps is None or width is None:
        cap = cv2.VideoCapture(mp4_path)
        try:
            if fps is None:
                fps_val = cap.get(cv2.CAP_PROP_FPS)
                fps = int(round(fps_val)) if fps_val and fps_val > 0 else 15
            if width is None:
                w_val = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                width = int(w_val) if w_val and w_val > 0 else 480
        finally:
            cap.release()
    
    print(f"Output gif width={width}, fps={fps}")

    base = f"fps={fps},scale={width}:-1:flags=lanczos"
    if remove_bg:
        key = _hex_to_ffmpeg(bg_color)
        base = f"{base},colorkey={key}:{similarity}:{blend},format=rgba"

    vf = (
        f"{base},"
        "split[s0][s1];"
        "[s0]palettegen=stats_mode=diff:reserve_transparent=1[p];"
        "[s1][p]paletteuse=new=1"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loglevel", "quiet", "-hide_banner",
        "-i", mp4_path,
        "-vf", vf,
        "-loop", "0",
        gif_path
    ]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    ap = argparse.ArgumentParser(description="Download a Twitter/X GIF (MP4) and convert to GIF.")
    ap.add_argument("url", help="Tweet/X URL containing the GIF/video")
    ap.add_argument("--fps", type=int, default=None, help="GIF frame rate (default: match source or 15)")
    ap.add_argument("--width", type=int, default=None, help="GIF width px (default: match source or 480)")
    ap.add_argument("-o", "--output", default=None, help="Output GIF path (default: YYYYMMDD-HHMMSS.gif in CWD)")

    ap.add_argument("-r", "--removebg", action="store_true",
                    help="Remove a solid background color to transparency (default white)")
    ap.add_argument("--color", default="#ffffff", help="Hex color to remove (default: #ffffff)")
    ap.add_argument("--similarity", type=float, default=0.12, help="Colorkey similarity 0..1 (default: 0.12)")
    ap.add_argument("--blend", type=float, default=0.00, help="Colorkey edge blend 0..1 (default: 0.00)")

    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        mp4_path = dl_video(args.url, tmp)
        if not os.path.exists(mp4_path):
            sys.exit("Could not download the video.")

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_gif = args.output or f"{timestamp}.gif"

        mp4_to_gif(
            mp4_path,
            out_gif,
            fps=args.fps,
            width=args.width,
            remove_bg=args.removebg,
            bg_color=args.color,
            similarity=args.similarity,
            blend=args.blend
        )
        print(f"Done: {out_gif}")

if __name__ == "__main__":
    main()
