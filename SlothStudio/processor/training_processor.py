import threading

from processor.yolo_trainer import YOLOTrainer
from processor.rtdetr_trainer import RTDETRTrainer
from processor.rfdetr_trainer import RFDETRTrainer

from processor.validation_processor import ValidationProcessor
from processor.models_export_processor import ModelsExportProcessor

class TrainingProcessor:

    def __init__(self, config, log_callback=None):

        self.config = self._normalize_config(config)

        self.log_callback = log_callback
        self.thread = None
        self.trainer = None

    def _normalize_config(self, cfg):

        dataset_yaml = cfg["dataset"]["dataset_yaml"]

        # FIX tuple-string bug
        if isinstance(dataset_yaml, str):
            dataset_yaml = dataset_yaml.strip()

            # remove ("path",) artifact
            if dataset_yaml.startswith("(") and dataset_yaml.endswith(")"):
                dataset_yaml = dataset_yaml.strip("()").replace(",", "").replace("'", "").strip()

        return {
            # dataset
            "dataset_yaml": dataset_yaml,

            # model
            "model_family": cfg["model"]["family"],
            "model_version": cfg["model"]["version"],
            "model_size": cfg["model"]["size"],

            # hyperparameters
            "epochs": int(cfg["hyperparameters"]["epochs"]),
            "batch_size": int(cfg["hyperparameters"]["batch_size"]),
            "image_size": int(cfg["hyperparameters"]["image_size"]),
            "amp_fp16": bool(cfg["hyperparameters"]["amp_fp16"]),

            # validation
            "run_validation": bool(cfg["validation"]["run_validation"]),
            "show_results": bool(cfg["validation"]["show_results"]),

            # export
            "export_onnx": bool(cfg["export"]["onnx"]),
            "export_tensorrt": bool(cfg["export"]["tensorrt"]),
        }

    def log(self, level, message):

        if self.log_callback:
            self.log_callback(level, message)

    def create_trainer(self):

        family = self.config["model_family"]

        if family == "YOLO":
            return YOLOTrainer(self.config, self.log_callback)

        if family == "RT-DETR":
            return RTDETRTrainer(self.config, self.log_callback)

        if family == "RF-DETR":
            return RFDETRTrainer(self.config, self.log_callback)

        raise ValueError(f"Unsupported model family: {family}")

    def start(self):

        self.thread = threading.Thread(target=self.worker, daemon=True)
        self.thread.start()

    def stop(self):

        if self.trainer:
            self.trainer.stop()

    def worker(self):

        try:

            self.log(
                "INFO",
                "TRAINING STARTED"
            )

            self.trainer = self.create_trainer()

            model_path = self.trainer.train()

            if self.config["run_validation"]:

                validator = ValidationProcessor(
                    self.log_callback
                )

                validator.validate(
                    model_path
                )

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
                "INFO",
                "PIPELINE COMPLETED"
            )

        except Exception as error:

            self.log(
                "ERROR",
                str(error)
            )
