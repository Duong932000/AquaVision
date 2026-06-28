from ultralytics import RTDETR
from ultralytics.utils import LOGGER

from processor.model_resolver import ModelResolver
from utils.ultralytics_log import UltralyticsUILogHandler

class RTDETRTrainer:
    def __init__(self, config, log_callback=None):

        self.config = config
        self.log_callback = log_callback
        self.logger_handler = None

    def log(self, level, message):

        if self.log_callback:self.log_callback(level, message)

    def stop(self):

        pass

    def train(self):

        model_name = ModelResolver.get_model_name(
            self.config["model_family"],
            self.config["model_version"],
            self.config["model_size"]
        )

        self.log(
            "INFO",
            f"Loading model: {model_name}"
        )

        self.logger_handler = UltralyticsUILogHandler(
            self.log_callback
        )

        LOGGER.addHandler(
            self.logger_handler
        )

        try:

            model = RTDETR(
                model_name
            )

            results = model.train(
                data=self.cfg["dataset_yaml"],
                epochs=self.cfg["epochs"],
                batch=self.cfg["batch_size"],
                imgsz=self.cfg["image_size"],
                amp=self.cfg["amp_fp16"]
            )

            best_model = (
                f"{results.save_dir}/weights/best.pt"
            )

            self.log(
                "INFO",
                f"Training completed: {best_model}"
            )

            return best_model

        finally:

            if self.logger_handler:

                LOGGER.removeHandler(
                    self.logger_handler
                )