
from rfdetr import RFDETR

class RFDETRTrainer:

    def __init__(self, cfg, log_callback=None):
        self.cfg = cfg
        self.log = log_callback

    def train(self):

        self._log("RF-DETR training start")

        model = RFDETR(
            model_size=self.cfg["model_size"]
        )

        model.train(
            dataset=self.cfg["dataset_yaml"],
            epochs=self.cfg["epochs"],
            batch_size=self.cfg["batch_size"],
            img_size=self.cfg["image_size"]
        )

        best_path = model.get_best_model_path()

        self._log(f"RF-DETR done: {best_path}")

        return best_path

    def _log(self, msg):
        if self.log:
            self.log(msg)