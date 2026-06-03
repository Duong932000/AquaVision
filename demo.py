from ultralytics import YOLO
import cv2
import yt_dlp


YOUTUBE_URL = "https://www.youtube.com/watch?v=MkaVR2VfpFE"

MODEL_PATH = "runs/detect/runs/koi_detection-3/weights/best.pt"

TRACKER = "bytetrack.yaml"

CONF = 0.25


def get_video_stream_url(url: str) -> str:

    ydl_opts = {
        "quiet": True,
        "format": "best[ext=mp4]/best",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return info["url"]

def main():

    print(f"Loading model: {MODEL_PATH}")

    model = YOLO(MODEL_PATH)

    print("Getting stream URL...")

    stream_url = get_video_stream_url(YOUTUBE_URL)

    print(stream_url)

    cap = cv2.VideoCapture(stream_url)

    if not cap.isOpened():
        raise RuntimeError("Cannot open video stream")

    print("Starting tracking...")

    while True:

        success, frame = cap.read()

        if not success:
            break

        results = model.track(
            frame,
            persist=True,
            tracker=TRACKER,
            conf=CONF,
            verbose=False,
        )

        annotated_frame = results[0].plot()

        cv2.imshow(
            "AquaVision - YOLO11 + ByteTrack",
            annotated_frame,
        )

        key = cv2.waitKey(1)

        if key == 27:
            break

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
