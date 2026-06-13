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
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime

SUPPORTED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
}

def load_json(json_file: Path) -> dict:
    if not json_file.exists():
        return {}
    
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(json_file: Path, data: dict):

    json_file.parent.mkdir(parents=True, exist_ok=True)

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_file_signature(file_path: Path) -> dict:

    stat = file_path.stat()

    return {
        "size": stat.st_size,
        "mtime": stat.st_mtime,
    }

def is_already_processed(file_path: Path, metadata: dict) -> bool:

    key = str(file_path.resolve())
    if key not in metadata:
        return False
    
    current = get_file_signature(file_path)

    saved = metadata[key]

    return (
        current["size"] == saved["size"]
        and current["mtime"] == saved["mtime"]
    )

def get_next_index(counter_file: Path) -> int:
    
    if not counter_file.exists():
        return 1
    
    data = load_json(counter_file)

    return data.get("next_index", 1)

def save_next_index(counter_file: Path, next_index: int):

    save_json(counter_file,
              {
                  "next_index": next_index
              },
              )

def extract_frames(video_path: Path, output_dir: Path, fish_type: str, start_index: int, frames_per_video: int) -> int:

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        print(f"[WARNING] Cannot open video: {video_path}")
        return 0

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames <= 0:
        cap.release()
        return 0

    if frames_per_video == 1:
        frame_positions = [total_frames // 2]
    else:
        frame_positions = [
            int(
                i * (total_frames - 1)
                / (frames_per_video - 1)
            )
            for i in range(frames_per_video)
        ]

    saved_count = 0

    for position in frame_positions:
        cap.set(cv2.CAP_PROP_POS_FRAMES, position)
        success, frame = cap.read()
        if not success:
            continue

        image_name = (
            f"{fish_type}_"
            f"{start_index + saved_count:06d}.jpg"
        )

        cv2.imwrite(
            str(output_dir / image_name),
            frame,
        )

        saved_count += 1

    cap.release()

    return saved_count

def process_raw_dataset():

    parser = argparse.ArgumentParser()
    parser.add_argument("--fish-type", required=True)
    parser.add_argument("--frames-per-video", type=int, default=15)
    args = parser.parse_args()

    fish_type = args.fish_type.lower()

    dataset_root = Path(f"datasets/{fish_type}")

    raw_images_dir = dataset_root / "raw" / "images"

    raw_videos_dir = dataset_root / "raw" / "videos"

    metadata_dir = dataset_root / "metadata"

    processed_videos_file = metadata_dir / "processed_videos.json"

    processed_images_file = metadata_dir / "processed_images.json"

    counter_file = metadata_dir / "dataset_counter.json"

    processed_videos = load_json(processed_videos_file)

    processed_images = load_json(processed_images_file)

    current_index = get_next_index(counter_file)

    batch_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_dir = dataset_root / "processed" / f"{fish_type}.{batch_timestamp}"
    
    output_dir.mkdir(parents=True, exist_ok=True)

    total_video_frames = 0
    total_copied_images = 0

    print("================================")
    print(" AquaVision Dataset Processor")
    print("================================")
    print(f"Fish Type : {fish_type}")
    print(f"Output    : {output_dir}")
    print()

    video_files = sorted(raw_videos_dir.rglob("*.mp4"))

    for video_file in video_files:
        if is_already_processed(video_file, processed_videos):
            print(f"[SKIP] {video_file.name}")
            continue

        extracted = extract_frames(
            video_path=video_file,
            output_dir=output_dir,
            fish_type=fish_type,
            start_index=current_index,
            frames_per_video=args.frames_per_video,
        )

        processed_videos[str(video_file.resolve())] = {
            **get_file_signature(
                video_file
            ),
            "processed_at":
                datetime.now().isoformat(),
            "frames_extracted":
                extracted,
        }

        current_index += extracted
        total_video_frames += extracted

        print(f"[VIDEO] "
            f"{video_file.name}"
            f" -> {extracted}"
        )

    if raw_images_dir.exists():
        image_files = sorted(
            [
                p
                for p in raw_images_dir.iterdir()
                if p.suffix.lower()
                in SUPPORTED_IMAGE_EXTENSIONS
            ]
        )

        for image_file in image_files:
            if is_already_processed(image_file, processed_images):
                print(f"[SKIP] {image_file.name}")
                continue

            image_name = f"{fish_type}_{current_index:06d}.jpg"

            shutil.copy2(image_file, output_dir / image_name)

            processed_images[str(image_file.resolve())] = {
                **get_file_signature(
                    image_file
                ),
                "processed_at":
                    datetime.now().isoformat(),
            }

            current_index += 1
            total_copied_images += 1

    save_json(processed_videos_file, processed_videos)
    save_json(processed_images_file, processed_images)

    save_next_index(counter_file, current_index)

    print("================================")
    print(" DATASET SUMMARY")
    print("================================")
    print(f"Frames extracted : {total_video_frames}")
    print(f"Images copied    : {total_copied_images}")
    print(f"Total samples    : {total_video_frames + total_copied_images}")
    print(f"Output folder    : {output_dir}")
    print("================================")


if __name__ == "__main__":

    process_raw_dataset()
