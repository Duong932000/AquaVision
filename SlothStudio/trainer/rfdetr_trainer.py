from datetime import datetime
from pathlib import Path

from rfdetr import RFDETRLarge, RFDETRMedium, RFDETRNano, RFDETRSmall

from trainer.base_trainer import BaseTrainer


class RFDETRTrainer(BaseTrainer):

    _MODEL_CLASSES = {
        "n": RFDETRNano,
        "s": RFDETRSmall,
        "m": RFDETRMedium,
        "l": RFDETRLarge,
    }

    def resolve_model_class(self):

        size = self.config["model"]["size"]

        model_cls = self._MODEL_CLASSES.get(size)

        if model_cls is None:
            raise ValueError(
                f"RF-DETR size '{size}' is not supported "
                f"(supported sizes: {', '.join(self._MODEL_CLASSES)})"
            )

        return model_cls

    def resolve_dataset_dir(self):

        dataset_path = Path(self.config["dataset"]["dataset_yaml"])

        if dataset_path.is_dir():
            return dataset_path

        return dataset_path.parent

    def stop(self):

        self.stop_event.set()

        self.log(
            "WARNING",
            "RF-DETR training cannot be interrupted mid-epoch; "
            "it will keep running until the current training call returns.",
        )

    def train(self):

        model_cls = self.resolve_model_class()
        dataset_dir = self.resolve_dataset_dir()

        self.log("INFO", f"Loading model: {model_cls.__name__}")

        self.model = model_cls()

        hyperparams = self.config["hyperparameters"]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("runs") / "rfdetr" / f"train-{timestamp}"

        self.model.train(
            dataset_dir=str(dataset_dir),
            epochs=hyperparams["epochs"],
            batch_size=hyperparams["batch_size"],
            resolution=hyperparams["image_size"],
            output_dir=str(output_dir),
        )

        best_model = output_dir / "checkpoint_best_total.pth"
        last_model = output_dir / "checkpoint_best_regular.pth"

        self.log("SUCCESS", "Training completed")

        return best_model, last_model
