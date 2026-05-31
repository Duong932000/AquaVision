
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

def youtube_video_downloader():

    parser = argparse.ArgumentParser(description="Download YouTube video for AquaVision dataset creation")

    # url of the YouTube video
    parser.add_argument("--url", required=True, help="YouTube URL")

    # fish type, e.g: "tilapia", "catfish", eel
    parser.add_argument("--fish-type", required=True, help="Type of fish in the video")

    parser.add_argument("--duration", type=int, default=300, help="Maximum duration in seconds")

    parser.add_argument("--output-dir", default="datasets/raw_videos", help="Output directory")

    args = parser.parse_args()

    output_dir = Path("datasets/raw/youtube")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_filename = (f"{args.fish_type.lower()}-{args.duration}s-{timestamp}.mp4")
    output_path = output_dir / output_filename

    print(f"[INFO] Fish Type : {args.fish_type}")
    print(f"[INFO] Duration  : {args.duration}s")
    print(f"[INFO] Output    : {output_path}")

    cmd = [
        "yt-dlp",
        "--format",
        (
            "bestvideo[height<=720][ext=mp4]"
            "+bestaudio[ext=m4a]"
            "/best[height<=720][ext=mp4]"
        ),
        "--merge-output-format",
        "mp4",
        "--download-sections",
        f"*0-{args.duration}",
        "-o",
        str(output_path),
        args.url,
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print("[ERROR] Download failed")
        sys.exit(1)

    print("[INFO] Download completed")
    print(f"[INFO] Saved to: {output_path}")

if __name__ == "__main__":
    youtube_video_downloader()