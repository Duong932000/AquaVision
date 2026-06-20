
import cv2
import yt_dlp
import threading
from ultralytics import YOLO


class InferenceProcessor:
    def __init__(self, config, frame_callback=None,log_callback=None):

        self.config = config
        self.frame_callback = frame_callback
        self.log_callback = log_callback

        self.running = False
        self.model = None
        self.capture = None

        self.inference_thread = None

    def start(self):

        if self.running:
            return

        self.running = True

        self.inference_thread = threading.Thread(target=self.run, daemon=True)

        self.inference_thread.start()

    def stop(self):

        self.running = False

        if self.capture is not None:
            self.capture.release()

        self.log("WARNING", "Inference stopped by user")

    def run(self):

        try:
            self.load_model()
            source = self.source_process()
            self.process_source(source)
            self.log("INFO", "Inference completed")
        except Exception as e:
            self.log("ERROR", str(e))
        finally:
            self.running = False
            if self.capture is not None:
                self.capture.release()
            self.log("INFO", "Inference finished")

    def log(self, level, message):

        if self.log_callback:
            self.log_callback(level, message)

    def load_model(self):

        model_config = self.config["model"]
        if model_config["type"] == "trained":
            model_path = model_config["path"]
        else:
            version = model_config["version"]
            size = model_config["size"]
            model_path = f"{version.lower()}{size}.pt"
        self.log("INFO", f"Loading model: {model_path}")
        self.model = YOLO(model_path)

    def source_process(self):

        source_config = self.config["source"]
        source_type = source_config["type"]
        items = source_config["items"]

        if not items:
            raise RuntimeError("No source selected")

        if source_type == "local":
            return items[0]

        if source_type == "youtube":
            youtube_url = items[0]
            self.log("INFO", "Resolving youtube stream ...")

            ydl_opts = {
                "quiet": True,
                "format": "best",
                "noplaylist": True,
                "extract_flat": False,
                "cookiefile": "/home/dacduong/Downloads/cookies.txt"
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=False)

            stream_url = info["url"]

            return stream_url

        raise RuntimeError(f"Unsupported source type: {source_type}")

    def process_source(self, source):

        detection_config = self.config["detection"]
        tracking_config = self.config["tracking"]
        runtime_config = self.config["runtime"]

        confidence = detection_config["confidence"]
        iou = detection_config["iou"]

        device = runtime_config["device"]

        if device == "Auto":
            device = None
        elif device == "CPU":
            device = "cpu"
        elif device == "CUDA":
            device = 0

        self.capture = cv2.VideoCapture(source)

        if not self.capture.isOpened():
            raise RuntimeError(f"Cannot open source: {source}")

        frame_count = 0

        tracker_enabled = tracking_config["enabled"]

        tracker_yaml = None

        if tracker_enabled:
            tracker_yaml = (
                "bytetrack.yaml"
                if tracking_config["tracker"] == "ByteTrack"
                else "botsort.yaml"
            )

        # running inference handling
        while self.running:
            success, frame = self.capture.read()
            if not success:
                break
            
            # tracking handling
            if tracker_enabled:
                results = self.model.track(frame,
                                           persist=True,
                                           conf=confidence,
                                           iou=iou,
                                           tracker=tracker_yaml,
                                           device=device,
                                           verbose=False)
            else:
                results = self.model.predict(frame,
                                             conf=confidence,
                                             iou=iou,
                                             device=device,
                                             verbose=False)
            annotated_frame = results[0].plot()
            frame_count += 1
            if self.frame_callback:
                self.frame_callback(annotated_frame)

            if frame_count % 300 == 0:
                self.log("INFO", f"Processed {frame_count} frames")

        self.capture.release()