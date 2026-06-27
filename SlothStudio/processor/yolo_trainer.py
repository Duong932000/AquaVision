from ultralytics import YOLO

from processor.model_resolver import ModelResolver

class YOLOTrainer:

    def __init__(self, cfg, log_callback=None):

        self.cfg = cfg
        self.log_callback = log_callback

    def train(self):

        model_name = ModelResolver.get_model_name(
            self.cfg["model_family"],
            self.cfg["model_version"],
            self.cfg["model_size"]
        )

        self.log(f"Loading model: {model_name}")

        model = YOLO(model_name)

        results = model.train(
            data=self.cfg["dataset_yaml"],
            epochs=self.cfg["epochs"],
            batch=self.cfg["batch_size"],
            imgsz=self.cfg["image_size"],
            amp=self.cfg["amp_fp16"]
        )

        return f"{results.save_dir}/weights/best.pt"

    def log(self, msg):
        if self.log_callback:
            self.log_callback(msg)