
from ultralytics import YOLO

from processor.base_trainer import BaseTrainer


class YOLOTrainer(BaseTrainer):

    def train(self):

        model_name = (
            f"{self.config['model_version']}"
            f"{self.config['model_size']}.pt"
        )

        self.log(f"Loading model: {model_name}\n")

        model = YOLO(model_name)

        model.train(
            data=self.config["dataset_yaml"],
            epochs=self.config["epochs"],
            batch=self.config["batch_size"],
            imgsz=self.config["imgsz"],
            amp=self.config["amp"],
            project="runs/train",
            name=self.config["project_name"]
        )

        self.log("YOLO training finished.\n")