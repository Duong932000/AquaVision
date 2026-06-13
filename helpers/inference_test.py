#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime

import argparse
import time

import cv2
import yt_dlp

from ultralytics import YOLO

DEFAULT_MODEL = (
    "runs/detect/train/weights/best.pt"
)

DEFAULT_TRACKER = "bytetrack.yaml"

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
}


def get_video_stream_url(url: str) -> str:

    ydl_opts = {
        "quiet": True,
        "format": "best[ext=mp4]/best",
    }

    with yt_dlp.YoutubeDL(
        ydl_opts
    ) as ydl:

        info = ydl.extract_info(
            url,
            download=False,
        )

    return info["url"]


def is_image_file(source: str) -> bool:

    path = Path(source)

    return (
        path.exists()
        and path.suffix.lower()
        in IMAGE_EXTENSIONS
    )


def create_capture(source: str):

    local_file = Path(source)

    if local_file.exists():

        print(
            f"[INFO] Local source detected"
        )

        cap = cv2.VideoCapture(
            str(local_file)
        )

    else:

        print(
            f"[INFO] YouTube URL detected"
        )

        stream_url = get_video_stream_url(
            source
        )

        cap = cv2.VideoCapture(
            stream_url
        )

    if not cap.isOpened():

        raise RuntimeError(
            f"Cannot open source: {source}"
        )

    return cap


def gui_available() -> bool:

    try:

        cv2.namedWindow(
            "test",
            cv2.WINDOW_NORMAL,
        )

        cv2.destroyWindow(
            "test"
        )

        return True

    except Exception:

        return False


def run_image(
    model: YOLO,
    image_path: str,
    conf: float,
):

    image = cv2.imread(
        image_path
    )

    if image is None:

        raise RuntimeError(
            f"Cannot load image: {image_path}"
        )

    results = model.predict(
        image,
        conf=conf,
        verbose=False,
    )

    annotated = image.copy()

    result = results[0]

    total_fish = 0

    if result.boxes is not None:

        total_fish = len(
            result.boxes
        )

        for box in result.boxes:

            x1, y1, x2, y2 = (
                box.xyxy[0]
                .cpu()
                .numpy()
                .astype(int)
            )

            score = float(
                box.conf[0]
            )

            cv2.rectangle(
                annotated,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2,
            )

            cv2.putText(
                annotated,
                f"{score:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

    cv2.putText(
        annotated,
        f"Fish: {total_fish}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    output_dir = Path(
        "outputs/inference"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        output_dir
        / f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    )

    cv2.imwrite(
        str(output_file),
        annotated,
    )

    print(
        f"[INFO] Saved: {output_file}"
    )

    if gui_available():

        cv2.imshow(
            "AquaVision",
            annotated,
        )

        cv2.waitKey(0)

        cv2.destroyAllWindows()


def run_video(
    model: YOLO,
    source: str,
    conf: float,
    tracker: str,
):

    cap = create_capture(
        source
    )

    width = int(
        cap.get(
            cv2.CAP_PROP_FRAME_WIDTH
        )
    )

    height = int(
        cap.get(
            cv2.CAP_PROP_FRAME_HEIGHT
        )
    )

    fps_input = cap.get(
        cv2.CAP_PROP_FPS
    )

    if fps_input <= 0:

        fps_input = 25

    output_dir = Path(
        "outputs/inference"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        output_dir
        / (
            "video_"
            + datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )
            + ".mp4"
        )
    )

    writer = cv2.VideoWriter(
        str(output_file),
        cv2.VideoWriter_fourcc(
            *"mp4v"
        ),
        fps_input,
        (width, height),
    )

    use_gui = gui_available()

    print(
        f"[INFO] GUI available: {use_gui}"
    )

    print(
        f"[INFO] Saving output:"
        f" {output_file}"
    )

    prev_time = time.time()

    while True:

        success, frame = cap.read()

        if not success:
            break

        results = model.track(
            frame,
            persist=True,
            tracker=tracker,
            conf=conf,
            verbose=False,
        )

        result = results[0]

        annotated = frame.copy()

        total_fish = 0

        if result.boxes is not None:

            total_fish = len(
                result.boxes
            )

            for box in result.boxes:

                x1, y1, x2, y2 = (
                    box.xyxy[0]
                    .cpu()
                    .numpy()
                    .astype(int)
                )

                score = float(
                    box.conf[0]
                )

                track_id = -1

                if (
                    hasattr(box, "id")
                    and box.id is not None
                ):
                    track_id = int(
                        box.id.item()
                    )

                cv2.rectangle(
                    annotated,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2,
                )

                label = (
                    f"ID:{track_id}"
                    f" {score:.2f}"
                )

                cv2.putText(
                    annotated,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )

        now = time.time()

        fps = 1.0 / max(
            now - prev_time,
            1e-6,
        )

        prev_time = now

        cv2.putText(
            annotated,
            f"Fish: {total_fish}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        cv2.putText(
            annotated,
            f"FPS: {fps:.1f}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        writer.write(
            annotated
        )

        if use_gui:

            cv2.imshow(
                "AquaVision",
                annotated,
            )

            key = cv2.waitKey(
                1
            )

            if key == 27:
                break

    writer.release()

    cap.release()

    cv2.destroyAllWindows()

    print()
    print(
        f"[INFO] Output saved:"
    )
    print(output_file)


def main():

    parser = argparse.ArgumentParser(
        description=
        "AquaVision Inference Test"
    )

    parser.add_argument(
        "--source",
        required=True,
    )

    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
    )

    parser.add_argument(
        "--tracker",
        default=DEFAULT_TRACKER,
    )

    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
    )

    args = parser.parse_args()

    print(
        f"[INFO] Loading model:"
        f" {args.model}"
    )

    model = YOLO(
        args.model
    )

    if is_image_file(
        args.source
    ):

        run_image(
            model,
            args.source,
            args.conf,
        )

    else:

        run_video(
            model,
            args.source,
            args.conf,
            args.tracker,
        )


if __name__ == "__main__":
    main()