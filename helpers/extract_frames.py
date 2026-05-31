#!/usr/bin/env python3

import cv2
import argparse
from pathlib import Path

def processor(video_path: Path, output_dir: Path, fps: float) -> int:

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    source_fps = cap.get(cv2.CAP_PROP_FPS)

    if source_fps <= 0:
        source_fps = 30

    frame_interval = max(int(source_fps / fps), 1)

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            output_file = (output_dir / f"{video_path.stem}_{saved_count:06d}.jpg")
            cv2.imwrite(str(output_file), frame)
            saved_count += 1
        frame_count += 1
    cap.release()

    return saved_count

def video_frame_extractor():

    parser = argparse.ArgumentParser(description="AquaVision Frame Extractor")
    parser.add_argument("--video-path",required=True,help="Path to input video")
    parser.add_argument("--fps", type=float, default=1.0, help="Frames per second to extract")
    args = parser.parse_args()

    video = Path(args.video_path)

    if not video.exists():
        print(f"[ERROR] Video not found: {video}")
        return

    frames_dir = Path("datasets/frames")

    fish_type = (video.stem.split("-")[0].strip().lower())
    output_dir = frames_dir / fish_type
    output_dir.mkdir(parents=True, exist_ok=True)

    print("========================================")
    print(" AquaVision Frame Extractor")
    print("========================================")
    print(f"[INFO] Video     : {video}")
    print(f"[INFO] Fish Type : {fish_type}")
    print(f"[INFO] FPS       : {args.fps}")
    print(f"[INFO] Output    : {output_dir}")

    extracted = processor(video_path=video, output_dir=output_dir, fps=args.fps)

    print(f"[INFO] Extracted frames: {extracted}")
    print("[INFO] Completed")

if __name__ == "__main__":

    video_frame_extractor()