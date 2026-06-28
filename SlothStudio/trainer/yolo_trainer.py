from pathlib import Path

from ultralytics import YOLO
from ultralytics.utils import LOGGER

from utils.ultralytics_log import UltralyticsUILogHandler


class YOLOTrainer:

    def __init__(
            self,
            config,
            log_callback=None):

        self.config = config

        self.log_callback = log_callback

        self.logger_handler = None

    def log(
            self,
            level,
            message):

        if self.log_callback:
            self.log_callback(
                level,
                message
            )

    def stop(self):

        #
        # TODO
        # future multiprocessing stop
        #
        pass

    def build_model_name(self):

        version = (
            self.config["model"]["version"]
        )

        size = (
            self.config["model"]["size"]
        )

        return (
            f"{version.lower()}{size}.pt"
        )

    def train(self):

        model_name = (
            self.build_model_name()
        )

        self.log(
            "INFO",
            f"Loading model: {model_name}"
        )

        self.logger_handler = (
            UltralyticsUILogHandler(
                self.log_callback
            )
        )

        LOGGER.addHandler(
            self.logger_handler
        )

        try:

            #
            # Auto download
            #
            model = YOLO(
                model_name
            )

            results = model.train(
                data=self.config["dataset"]["dataset_yaml"],

                epochs=self.config["hyperparameters"]["epochs"],

                batch=self.config["hyperparameters"]["batch_size"],

                imgsz=self.config["hyperparameters"]["image_size"],

                amp=self.config["hyperparameters"]["amp_fp16"]
            )

            save_dir = Path(
                results.save_dir
            )

            best_model = (
                save_dir
                / "weights"
                / "best.pt"
            )

            last_model = (
                save_dir
                / "weights"
                / "last.pt"
            )

            self.log(
                "SUCCESS",
                "Training completed"
            )

            return best_model, last_model

        finally:

            if self.logger_handler:

                LOGGER.removeHandler(
                    self.logger_handler
                )