#!/usr/bin/env python3

"""
process_raw_dataset.py

AquaVision Dataset Processor

Purpose
-------
Convert raw videos and raw images into a single dataset folder
ready for annotation in CVAT or Roboflow.

Workflow
--------
raw/
├── videos/
│   └── **/*.mp4
│
└── images/
    └── *.jpg

        ↓

processed/
└── dataset.<fish_type>.v<version>/
    ├── koi_000001.jpg
    ├── koi_000002.jpg
    ├── koi_000003.jpg
    └── ...

Features
--------
- Recursive video discovery
- Uniform frame extraction per video
- Copy raw images
- Automatic sequential renaming
- Dataset versioning support
- Annotation-ready output

Example
-------
python process_raw_dataset.py \
    --fish-type koi \
    --frames-per-video 15 \
    --version 1
"""

import cv2
import shutil
import argparse
from pathlib import Path

SUPPORTED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
}

def extract_frames(video_path: Path,
                   output_dir: Path,
                   fish_type: str,
                   start_index: int,
                   frames_per_video: int) -> int:
    """
    Extract a fixed number of frames uniformly distributed
    across a video.
    """

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        print(f"[WARNING] Cannot open video: {video_path}")
        return 0

    total_frames = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    if total_frames <= 0:
        cap.release()
        print(f"[WARNING] Invalid frame count: {video_path}")
        return 0

    frame_positions = []

    if frames_per_video == 1:
        frame_positions = [total_frames // 2]
    else:
        for i in range(frames_per_video):
            position = int(i * (total_frames - 1) / (frames_per_video - 1))
            frame_positions.append(position)

    saved_count = 0
    for position in frame_positions:
        cap.set(cv2.CAP_PROP_POS_FRAMES, position)
        success, frame = cap.read()

        if not success:
            continue

        image_name = f"{fish_type}_{start_index + saved_count:06d}.jpg"
        image_path = output_dir / image_name

        cv2.imwrite(str(image_path), frame)
        saved_count += 1

    cap.release()

    return saved_count

def copy_images(images_dir: Path,
                output_dir: Path,
                fish_type: str,
                start_index: int) -> int:
    """
    Copy all images from raw/images and rename them.
    """

    image_files = sorted(
        [
            path
            for path in images_dir.iterdir()
            if path.suffix.lower()
            in SUPPORTED_IMAGE_EXTENSIONS
        ]
    )

    copied_count = 0

    for image_file in image_files:
        image_name = f"{fish_type}_{start_index + copied_count:06d}.jpg"
        destination = output_dir / image_name
        shutil.copy2(image_file, destination,)
        copied_count += 1

    return copied_count

def process_raw_dataset():

    parser = argparse.ArgumentParser(description="AquaVision Dataset Processor")
    parser.add_argument("--fish-type", required=True, help="Fish type (e.g. koi, eel)")
    parser.add_argument("--frames-per-video", type=int, default=15, help="Number of frames extracted from each video")
    parser.add_argument("--version", type=int, default=1, help="Dataset version")
    args = parser.parse_args()

    fish_type = args.fish_type.lower()
    dataset_root = Path(f"datasets/{fish_type}")

    raw_images_dir = dataset_root/ "raw" / "images"
    raw_videos_dir = dataset_root / "raw" / "videos"

    output_dir = dataset_root / "processed" / f"dataset.{fish_type}.v{args.version}"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("========================================")
    print(" AquaVision Dataset Processor")
    print("========================================")
    print(f"Fish Type       : {fish_type}")
    print(f"Dataset Version : {args.version}")
    print(f"Frames / Video  : {args.frames_per_video}")
    print(f"Output          : {output_dir}")
    print()

    current_index = 1
    total_video_frames = 0

    video_files = sorted(raw_videos_dir.rglob("*.mp4"))

    print(f"[INFO] Found {len(video_files)} video(s)")

    for video_file in video_files:
        extracted = extract_frames(
            video_path=video_file,
            output_dir=output_dir,
            fish_type=fish_type,
            start_index=current_index,
            frames_per_video=args.frames_per_video,
        )

        current_index += extracted
        total_video_frames += extracted

        print(f"[VIDEO] {video_file.name} -> {extracted} frame(s)")

    total_copied_images = 0

    if raw_images_dir.exists():
        total_copied_images = copy_images(
            images_dir=raw_images_dir,
            output_dir=output_dir,
            fish_type=fish_type,
            start_index=current_index,
        )

        current_index += total_copied_images

    print(f"[INFO] Copied {total_copied_images} image(s)")


    print("========================================")
    print(" DATASET SUMMARY")
    print("========================================")
    print(f"Frames extracted : {total_video_frames}")
    print(f"Images copied    : {total_copied_images}")
    print(f"Total samples    : {total_video_frames + total_copied_images}")
    print(f"Dataset folder   : {output_dir}")
    print("========================================")

if __name__ == "__main__":

    process_raw_dataset()
