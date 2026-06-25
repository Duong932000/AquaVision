from ultralytics import YOLO


class ModelsExportProcessor:

    def __init__(self,
                 log_callback=None):

        self.log_callback = log_callback

    def log(self, message):

        if self.log_callback:
            self.log_callback(message)

    def export_onnx(self,
                    model_path):

        self.log(
            "Export ONNX started...\n"
        )

        model = YOLO(model_path)

        model.export(
            format="onnx"
        )

        self.log(
            "ONNX export completed.\n"
        )

    def export_tensorrt(self,
                        model_path):

        self.log(
            "Export TensorRT started...\n"
        )

        model = YOLO(model_path)

        model.export(
            format="engine"
        )

        self.log(
            "TensorRT export completed.\n"
        )