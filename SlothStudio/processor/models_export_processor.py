class ModelsExportProcessor:

    def __init__(self, log_callback=None):
        self.log = log_callback

    def export_onnx(self, model_path):
        self._log(f"Export ONNX: {model_path}")

    def export_tensorrt(self, model_path):
        self._log(f"Export TensorRT: {model_path}")

    def _log(self, msg):
        if self.log:
            self.log(msg)