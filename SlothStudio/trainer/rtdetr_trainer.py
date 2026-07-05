from pathlib import Path

from ultralytics import RTDETR
from ultralytics.utils import LOGGER

from processor.model_resolver import ModelResolver
from trainer.base_trainer import BaseTrainer
from utils.ultralytics_log import UltralyticsUILogHandler


class RTDETRTrainer(BaseTrainer):

    def __init__(self, config, log_callback=None):
        super().__init__(config, log_callback)

        self.logger_handler = None

    def build_model_name(self):

        model_cfg = self.config["model"]

        return ModelResolver.get_model_name(
            model_cfg["family"],
            model_cfg["version"],
            model_cfg["size"],
        )

    def _on_epoch_end(self, trainer):

        if self.stop_event.is_set():
            trainer.stop = True

    def train(self):

        model_name = self.build_model_name()

        self.log("INFO", f"Loading model: {model_name}")

        self.logger_handler = UltralyticsUILogHandler(self.log_callback)
        LOGGER.addHandler(self.logger_handler)

        try:
            self.model = RTDETR(model_name)
            self.model.add_callback("on_train_epoch_end", self._on_epoch_end)

            hyperparams = self.config["hyperparameters"]

            results = self.model.train(
                data=self.config["dataset"]["dataset_yaml"],
                epochs=hyperparams["epochs"],
                batch=hyperparams["batch_size"],
                imgsz=hyperparams["image_size"],
                amp=hyperparams["amp_fp16"],
            )

            save_dir = Path(results.save_dir)

            best_model = save_dir / "weights" / "best.pt"
            last_model = save_dir / "weights" / "last.pt"

            self.log("SUCCESS", "Training completed")

            return best_model, last_model

        finally:

            if self.logger_handler:
                LOGGER.removeHandler(self.logger_handler)
