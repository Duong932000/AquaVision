from pathlib import Path
import argparse

import cv2
import yt_dlp
from ultralytics import YOLO


MODEL_PATH = "runs/detect/runs/koi_detection-5/weights/best.pt"
TRACKER = "bytetrack.yaml"
CONF = 0.25


def get_video_stream_url(url: str) -> str:

    ydl_opts = {
        "quiet": True,
        "format": "best[ext=mp4]/best",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(
            url,
            download=False,
        )

    return info["url"]


def create_capture(source: str) -> cv2.VideoCapture:

    local_file = Path(source)

    if local_file.exists():

        print(f"[INFO] Local video detected")
        print(f"[INFO] Source: {local_file}")

        cap = cv2.VideoCapture(
            str(local_file)
        )

    else:

        print(f"[INFO] YouTube URL detected")
        print(f"[INFO] Source: {source}")

        stream_url = get_video_stream_url(
            source
        )

        print(
            f"[INFO] Stream URL acquired"
        )

        cap = cv2.VideoCapture(
            stream_url
        )

    if not cap.isOpened():

        raise RuntimeError(
            f"Cannot open source: {source}"
        )

    return cap


def main():

    parser = argparse.ArgumentParser(
        description="AquaVision Fish Tracking"
    )

    parser.add_argument(
        "--source",
        required=True,
        help="Local video path or YouTube URL",
    )

    parser.add_argument(
        "--model",
        default=MODEL_PATH,
        help="YOLO model path",
    )

    parser.add_argument(
        "--conf",
        type=float,
        default=CONF,
        help="Confidence threshold",
    )

    args = parser.parse_args()

    print(
        f"[INFO] Loading model: {args.model}"
    )

    model = YOLO(args.model)

    cap = create_capture(
        args.source
    )

    print(
        "[INFO] Starting tracking..."
    )

    while True:

        success, frame = cap.read()

        if not success:
            break

        results = model.track(
            frame,
            persist=True,
            tracker=TRACKER,
            conf=args.conf,
            verbose=False,
        )

        annotated_frame = frame.copy()

        total_fish = 0

        result = results[0]

        if result.boxes is not None:

            total_fish = len(result.boxes)

            for box in result.boxes:

                x1, y1, x2, y2 = (
                    box.xyxy[0]
                    .cpu()
                    .numpy()
                    .astype(int)
                )

                cv2.rectangle(
                    annotated_frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2,
                )

        cv2.putText(
            annotated_frame,
            f"Total Fish: {total_fish}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        cv2.imshow(
            "AquaVision - Fish Tracking",
            annotated_frame,
        )

        key = cv2.waitKey(1)

        if key == 27:
            break

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()