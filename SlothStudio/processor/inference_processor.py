
import os
import cv2
import json
import yt_dlp
import threading
from pathlib import Path
from ultralytics import YOLO
from datetime import datetime

# internal modules
from utils.load_config import _get_root_dir

class InferenceProcessor:
    def __init__(self, config, frame_callback=None, log_callback=None):
        
        # varible of json config (come from UI configure)
        self.inference_config = config
        self.frame_callback = frame_callback
        self.log_callback = log_callback

        # flag for processing
        self.running = False
        self.model = None
        self.capture = None
        self.inference_thread = None

        # ultralytic cache dir
        self.ultralytic_cache_dir = "~/.cache/ultralytics/models"

        # get root dir
        self.root_dir = _get_root_dir()
        self.output_dir = None
        self.video_writer = None
        self.saved_frame_count = 0
        self.save_frame_interval = 300 # 10s / 30 FPS

    def load_config(self):

        # get source config
        self.source_cfg = self.inference_config["source"]
        self.source_type = self.source_cfg["type"]
        self.source_items = self.source_cfg["items"]

        # get model config
        self.model_cfg = self.inference_config["model"]
        self.model_type = self.model_cfg["type"]

        # get tracking config
        self.tracking_cfg = self.inference_config["tracking"]
        self.tracking_enabled = self.tracking_cfg["enabled"]
        self.tracker = self.tracking_cfg["tracker"]

        # get detection parameter config
        self.detection_cfg = self.inference_config["detection"]
        self.confidence = self.detection_cfg["confidence"]
        self.iou = self.detection_cfg["iou"]
        self.image_size = self.detection_cfg.get("image_size", 1280)
        self.fp16 = self.detection_cfg.get("fp16", False)
        self.max_detection = self.detection_cfg.get("max_detection", 100)

        # get output config
        self.output_cfg = self.inference_config["output"]
        self.save_video = self.output_cfg["save_video"]
        self.save_frames = self.output_cfg["save_frames"]

        # get device runtime config
        self.runtime_cfg = self.inference_config["runtime"]
        self.device = self.runtime_cfg["device"]

    def start(self):

        if self.running:
            return

        self.running = True

        self.inference_thread = threading.Thread(target=self.run, daemon=True)

        self.inference_thread.start()

    def stop(self):

        self.running = False

        # if self.capture is not None:
        #     self.capture.release()

        self.log("WARNING", "Inference stopped by user")

    def run(self):

        try:
            # load inference config to run
            self.load_config()

            # setup output dir
            self.setup_output_dir()

            # load model
            self.load_model()

            # process source file to inference
            source = self.source_handling()

            # inference model with source file
            self.inference_model(source)

        except Exception as e:
            self.log("ERROR", str(e))
            raise RuntimeError(f"Error: {e}")

        finally:
            self.running = False
            if self.capture is not None:
                self.capture.release()
            if self.video_writer is not None:
                self.video_writer.release()
                self.video_writer = None

            self.log("INFO", "Inference finished")

    def log(self, level, message):

        if self.log_callback:
            self.log_callback(level, message)

    def load_model(self):

        # trained model
        if self.model_type == "trained": # trained model is local file
            model_path = self.model_cfg["path"]
            if not os.path.exists(model_path):
                self.log("ERROR", f"Model not found at: {model_path}")
            self.log("INFO", f"Loading trained model: {model_path}")
            self.model = YOLO(model_path)
            return

        # pretrained model
        version = self.model_cfg["version"]
        size = self.model_cfg["size"]
        model_name = f"{version.lower()}{size}.pt"
        self.model = self.pretrained_model_handling(model_name)

    def pretrained_model_handling(self, model_name):
        
        model_dir = os.path.expanduser(self.ultralytic_cache_dir)
        os.makedirs(model_dir, exist_ok=True)

        model_path = os.path.join(model_dir, model_name)
        if os.path.exists(model_path):
            self.log(f"INFO", f"Pretrained model found locally: {model_path}")
            return YOLO(model_path)
        
        self.log("INFO", f"Downloading pretrained model: {model_name}")

        # ultralytics auto-dowloading mechanism
        model = YOLO(model_name)

        self.log("INFO", f"Downloaded & loaded: {model_name}")

        return model

    def source_handling(self):

        if not self.source_items:
            self.log("ERROR", "No source selected")

        if self.source_type == "local":
            return self.source_items[0]

        if self.source_type == "youtube":
            url = self.source_items[0]
            self.log("INFO", "Resolving youtube stream")

            # processing cookies of youtube
            cookies_path = self.cookies_handling()

            # youtube streaming config
            ydl_opts = {
                "quiet": True,
                "format": "best",
                "noplaylist": True,
                "extract_flat": False,
            }
            
            # Append cookie file
            if cookies_path:
                ydl_opts["cookiesfile"] = cookies_path
            else:
                self.log("WARNING", "Running without cookies (may fail for restricted videos)")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            return info["url"]

        self.log("ERROR", f"Unsupported url: {url}")
    
        return None

    def cookies_handling(self):

        cookies_path = Path(self.root_dir) / "cookies.txt"
        if not cookies_path.exists():
            self.log("ERROR", f"No cookies file found: {cookies_path}")
            self.log("WARNING", f"Export cookies file to: {cookies_path}")
            return None

        self.log("INFO", f"Using cookies file: {cookies_path}")
        return str(cookies_path)

    def inference_model(self, source):
        
        device = self.device
        if device == "Auto":
            device = None
        elif device == "CPU":
            device = "cpu"
        elif device == "CUDA":
            device = 0

        # using opencv to process source, raise log if error
        self.capture = cv2.VideoCapture(source)
        if not self.capture.isOpened():
            self.log("ERROR", f"Cannot open source: {source}")
            raise RuntimeError(f"Cannot open source: {source}")

        source_fps = self.capture.get(cv2.CAP_PROP_FPS)
        if source_fps <= 0:
            source_fps = 30

        self.save_frame_interval = int(source_fps * 10)
        self.log("INFO", f"Frame save interval: {self.save_frame_interval} frames (~10 seconds)")

        # select tracker yaml file to support tracking with YOLO
        tracker_yaml = None
        tracking_enabled = self.tracking_enabled
        tracker = self.tracker
        if tracking_enabled:
            if tracker == "BoT-SORT":
                tracker_yaml = "botsort.yaml"
            elif tracker == "ByteTrack":
                tracker_yaml = "bytetrack.yaml"
            elif tracker == "Deep OC-SORT":
                tracker_yaml = "deepocsort.yaml"
            elif tracker == "OC-SORT":
                tracker_yaml = "ocsort.yaml"
            elif tracker == "FastTracker":
                tracker_yaml = "fasttrack.yaml"
            else:
                tracker_yaml = "tracktrack.yaml"

        video_writer_initialized = False

        frame_count = 0

        # running inference handling
        while self.running:
            ret, frame = self.capture.read()
            if not ret:
                break
            
            # tracking handling
            if tracking_enabled:
                # activate tracking mode
                results = self.model.track(frame,
                                           persist=True,
                                           conf=self.confidence,
                                           iou=self.iou,
                                           imgsz=self.image_size,
                                           max_det=self.max_detection,
                                           half=self.fp16,
                                           tracker=tracker_yaml,
                                           device=device,
                                           verbose=False)
            else:
                # activate predict mode, not tracking
                results = self.model.predict(frame,
                                             conf=self.confidence,
                                             iou=self.iou,
                                             imgsz=self.image_size,
                                             max_det=self.max_detection,
                                             half=self.fp16,
                                             device=device,
                                             verbose=False)

            annotated_frame = results[0].plot()

            # output video process
            if self.save_video and not video_writer_initialized:
                self.output_video_writer(annotated_frame)
                video_writer_initialized = True

            if self.save_video and self.video_writer is not None:
                self.video_writer.write(annotated_frame)

            # output frame process
            if (self.save_frames and frame_count % self.save_frame_interval == 0):
                frame_path = self.output_dir / f"frame_{frame_count:06d}.jpg"
                cv2.imwrite(str(frame_path), annotated_frame)
                self.saved_frame_count += 1

            # UI call back
            if self.frame_callback:
                self.frame_callback(annotated_frame)

            frame_count += 1

            if frame_count % 100 == 0:
                self.log("INFO", f"Processed {frame_count} frames")

        self.capture.release()
        self.log("INFO", f"Total processed frames: {frame_count}")

    def setup_output_dir(self):

        if not self.save_video and not self.save_frames:
            return
        
        # get timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # config path of output
        self.output_dir = Path(self.root_dir / "outputs" / "inference" / f"inference-{timestamp}")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # log output
        self.log("INFO", f"Output directory: {self.output_dir}")
        
        self.export_inference_config()

    def export_inference_config(self):

        config_path = self.output_dir / "config.json"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(self.inference_config, f, indent=4, ensure_ascii=False)

        self.log("INFO", f"Exported config.json at: {config_path}")

    def output_video_writer(self, frame):

        if not self.save_video:
            return
        
        height, width = frame.shape[:2]

        video_path = self.output_dir / "inference_output.mp4"

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        self.video_writer = cv2.VideoWriter(str(video_path), fourcc, 30, (width, height))

        self.log("INFO", f"Video recording: {video_path}")

    def log_config_summary(self):

        # log title
        self.log("INFO", "== Inference Config Summary ==")

        # log source
        self.log("INFO", f"Source: {self.source_type}")
        
        # log model
        if self.model_type == "trained":
            model_info = f'trained {self.model_cfg["path"]}'
        else:
            model_info = f'pretrained {self.model_cfg["version"]}{self.model_cfg["size"]}'
        self.log("INFO", f"Model: {model_info}")

        # log tracking
        tracking_info = f'{self.tracking_cfg["tracker"]} | enabled={self.tracking_enabled}'
        self.log("INFO", f"Tracker: {tracking_info}")

        # log detection
        self.log("INFO", f"Conf / IoU: {self.confidence} / {self.iou}")
        self.log("INFO", f"Image Size: {self.image_size} | FP16: {self.fp16} | MaxDet: {self.max_detection}")

        # log runtime
        self.log("INFO", f"Device: {self.device}")

        # log output
        self.log("INFO", f"Output: video ={self.save_video}, frames={self.save_frames}")

        # log end
        self.log("INFO", "==============================")
