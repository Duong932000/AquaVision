#!/usr/bin/env python3

"""
youtube_video_downloader.py

Download a specific segment from a YouTube video for AquaVision dataset collection.

Features:
- Download only a selected segment
- Maximum resolution: 1080p
- Auto-create dataset folders
- Fish type aware
- Human-readable start time

Examples:

python youtube_video_downloader.py \
    --url "https://www.youtube.com/watch?v=xxxxx" \
    --fish-type koi_fish

python youtube_video_downloader.py \
    --url "https://www.youtube.com/watch?v=xxxxx" \
    --fish-type koi_fish \
    --start-time 01:45 \
    --duration 120

python youtube_video_downloader.py \
    --url "https://www.youtube.com/watch?v=xxxxx" \
    --fish-type eel \
    --start-time 00:05:30 \
    --duration 180
"""

import argparse
import subprocess
import sys

from pathlib import Path
from datetime import datetime


def time_to_seconds(time_str: str) -> int:
    """
    Convert time string to seconds.

    Supported formats:
        MM:SS
        HH:MM:SS

    Examples:
        01:45 -> 105
        05:20 -> 320
        01:02:15 -> 3735
    """

    parts = time_str.strip().split(":")

    if len(parts) == 2:
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds

    if len(parts) == 3:
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds

    raise ValueError(
        f"Invalid time format: {time_str}. "
        f"Use MM:SS or HH:MM:SS"
    )


def format_filename_time(time_str: str) -> str:
    """
    Convert human readable time into filename friendly format.

    Example:
        01:45 -> 01m45s
        01:02:15 -> 01h02m15s
    """

    parts = time_str.strip().split(":")

    if len(parts) == 2:
        mm, ss = parts
        return f"{mm}m{ss}s"

    if len(parts) == 3:
        hh, mm, ss = parts
        return f"{hh}h{mm}m{ss}s"

    return "unknown"


def youtube_video_downloader():

    # Command-line argument parsing
    parser = argparse.ArgumentParser(description="Download YouTube video segment for AquaVision dataset collection")
    parser.add_argument("--url", required=True, help="YouTube video URL")
    parser.add_argument("--fish-type", required=True, help="Fish type (e.g. koi_fish, eel, tilapia)")
    parser.add_argument("--start-time", default="00:00", help="Start time (MM:SS or HH:MM:SS)")
    parser.add_argument("--duration", type=int, default=300, help="Duration to download in seconds")
    parser.add_argument("--max-resolution", default="best", help="Maximum video resolution (e.g. 1080p, 720p, best)")
    parser.add_argument("--output-dir", default=None, help="Custom output directory")
    args = parser.parse_args()

    start_seconds = time_to_seconds(args.start_time)
    end_seconds = start_seconds + args.duration

    if args.max_resolution == "best":
        format_string = (
            "bestvideo[vcodec*=avc1]+bestaudio"
            "/bestvideo+bestaudio"
            "/best"
        )
    else:
        format_string = (
            f"bestvideo[height<={args.max_resolution}]"
            "+bestaudio"
            "/best"
        )

    if args.output_dir is None:
        output_dir = Path(f"datasets/{args.fish_type.lower()}/raw/videos")

    else:
        output_dir = Path(args.output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    start_label = format_filename_time(args.start_time)

    output_filename = (
        f"{args.fish_type.lower()}"
        f"-start-{start_label}"
        f"-duration-{args.duration}s"
        f"-{timestamp}.mp4"
    )

    output_path = output_dir / output_filename

    print("===================================")
    print(" AquaVision Dataset Downloader")
    print("===================================")
    print(f"Fish Type : {args.fish_type}")
    print(f"Start Time: {args.start_time}")
    print(f"Duration  : {args.duration}s")
    print(f"Output    : {output_path}")

    cmd = [
        "yt-dlp",
        "--format",
        format_string,
        "--merge-output-format",
        "mp4",
        "--download-sections",
        f"*{start_seconds}-{end_seconds}",
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
