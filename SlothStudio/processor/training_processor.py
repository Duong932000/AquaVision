
import shutil
import threading
from pathlib import Path
from datetime import datetime

# internal modules
from utils.load_config import _get_root_dir
from trainer.yolo_trainer import YOLOTrainer
from trainer.rtdetr_trainer import RTDETRTrainer
from trainer.rfdetr_trainer import RFDETRTrainer
# from processor.validation_processor import ValidationProcessor
# from processor.models_export_processor import ModelsExportProcessor

class TrainingProcessor:

    TRAINER_CLASSES = {
        "YOLO": YOLOTrainer,
        "RT-DETR": RTDETRTrainer,
        "RF-DETR": RFDETRTrainer,
    }
    def __init__(self, config, log_callback=None):

        self.config = config

        self.log_callback = log_callback

        self.thread = None

        self.trainer = None

        self.running = False

        # get root dir
        self.root_dir = _get_root_dir()
        self.output_dir = None

    def log(self, level, message):

        if self.log_callback:
            self.log_callback(level, message)

    def create_trainer(self):

        model_family = self.config["model"]["family"]

        trainer_cls = self.TRAINER_CLASSES.get(model_family)

        if trainer_cls is None:
            raise RuntimeError(f"Unsupported model family {model_family}")

        return trainer_cls(self.config, self.log_callback)
    
    def start(self):

        if self.running:
            self.log("WARNING", "Training model process already running")
            return
        
        self.running = True

        self.setup_output_dir()

        self.thread = threading.Thread(target=self.worker, daemon=True)
        self.thread.start()

    def stop(self):

        self.running = False

        if self.trainer:
            self.trainer.stop()

    def setup_output_dir(self):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.output_dir = (Path(self.root_dir) / "outputs" / "train" / f"train-{timestamp}")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.log("INFO", f"Output directory: {self.output_dir}")

    def copy_training_artifacts(self, best_model, last_model):

        if best_model.exists():
            shutil.copy2(best_model, self.output_dir / "best.pt")
            self.log("INFO",f"Saved best.pt")

        if last_model.exists():
            shutil.copy2(last_model, self.output_dir / "last.pt")
            self.log("INFO", f"Saved last.pt")

    def worker(self):

        try:
            self.log("INFO", "=" * 70)
            self.log("INFO", "TRAINING STARTED")
            self.log("INFO", "=" * 70)

            # perform training
            self.trainer = self.create_trainer()
            best_model, last_model = self.trainer.train()
            self.copy_training_artifacts(best_model, last_model)

            # # validation model after training
            # if self.config["validation"]["run_validation"]:
            #     validator = ValidationProcessor(self.config, self.log_callback)
            #     validator.run_validate(result.best_model)

            # # export model onnx
            # if self.config["export"]["onnx"]:
            #     exporter = ModelsExportProcessor(result.best_model, self.log_callback)
            #     exporter.export_onnx()

            # if self.config["export"]["tensorrt"]:
            #     exporter = ModelsExportProcessor(result.best_model, self.log_callback)
            #     exporter.export_tensorrt()

            self.log("SUCCESS", "TRAINING COMPLETED")

        except Exception as e:
            self.log("ERROR", str(e))
        finally:
            self.running = False