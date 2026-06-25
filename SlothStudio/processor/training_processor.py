import threading

from processor.yolo_trainer import YOLOTrainer
from processor.rtdetr_trainer import RTDETRTrainer
from processor.rfdetr_trainer import RFDETRTrainer

from processor.validation_processor import ValidationProcessor
from processor.models_export_processor import ModelsExportProcessor

class TrainingProcessor:

    def __init__(self,
                 config,
                 log_callback=None):

        self.config = config

        self.log_callback = log_callback

        self.thread = None

        self.trainer = None

    def log(self, message):

        if self.log_callback:
            self.log_callback(message)

    def create_trainer(self):

        family = self.config["model_family"]

        if family == "YOLO":

            return YOLOTrainer(
                self.config,
                self.log_callback
            )

        elif family == "RT-DETR":

            return RTDETRTrainer(
                self.config,
                self.log_callback
            )

        elif family == "RF-DETR":

            return RFDETRTrainer(
                self.config,
                self.log_callback
            )

        raise RuntimeError(
            f"Unsupported model family: {family}"
        )
    
    def start(self):

        self.thread = threading.Thread(
            target=self._worker,
            daemon=True
        )

        self.thread.start()

    def stop(self):

        if self.trainer:

            self.trainer.stop()

    def _worker(self):

        try:

            self.log(
                "===================================\n"
            )

            self.log(
                "Training Started\n"
            )

            self.log(
                "===================================\n"
            )

            self.trainer = self.create_trainer()

            self.trainer.train()

            model_path = (
                f"runs/train/"
                f"{self.config['project_name']}/weights/best.pt"
            )

            #
            # Validation
            #
            if self.config["run_validation"]:

                validator = ValidationProcessor(
                    self.log_callback
                )

                validator.validate(
                    model_path
                )

            #
            # Export
            #
            exporter = ModelsExportProcessor(
                self.log_callback
            )

            if self.config["export_onnx"]:

                exporter.export_onnx(
                    model_path
                )

            if self.config["export_tensorrt"]:

                exporter.export_tensorrt(
                    model_path
                )

            self.log(
                "\nTraining Pipeline Completed.\n"
            )

        except Exception as error:

            self.log(
                f"\nERROR:\n{error}\n"
            )