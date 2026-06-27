
from ultralytics import RTDETR


class RTDETRTrainer:

    def __init__(self, cfg, log_callback=None):
        self.cfg = cfg
        self.log = log_callback

    def train(self):

        model = RTDETR(f"rtdetr-{self.cfg['model_size']}.pt")

        self._log("RT-DETR training start")

        results = model.train(
            data=self.cfg["dataset_yaml"],
            epochs=self.cfg["epochs"],
            batch=self.cfg["batch_size"],
            imgsz=self.cfg["image_size"],
            amp=self.cfg["amp_fp16"],
            project="runs/train",
            name=f"rtdetr_{self.cfg['model_size']}",
            device=0
        )

        best_path = f"{results.save_dir}/weights/best.pt"

        self._log(f"RT-DETR done: {best_path}")

        return best_path

    def _log(self, msg):
        if self.log:
            self.log(msg)