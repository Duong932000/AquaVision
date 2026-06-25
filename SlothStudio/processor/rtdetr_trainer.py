
from ultralytics import RTDETR

from processor.base_trainer import BaseTrainer


class RTDETRTrainer(BaseTrainer):

    def train(self):

        version = self.config["model_version"]

        size = self.config["model_size"]

        if version == "RT-DETR":
            model_name = f"rtdetr-{size}.pt"
        else:
            model_name = f"rtdetrv2-{size}.pt"

        self.log(f"Loading model: {model_name}\n")

        model = RTDETR(model_name)

        model.train(
            data=self.config["dataset_yaml"],
            epochs=self.config["epochs"],
            batch=self.config["batch_size"],
            imgsz=self.config["imgsz"]
        )

        self.log("RT-DETR training finished.\n")