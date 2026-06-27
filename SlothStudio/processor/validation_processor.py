class ValidationProcessor:

    def __init__(self, log_callback=None):
        self.log = log_callback

    def validate(self, model_path):
        self._log(f"Validating: {model_path}")
        self._log("Validation completed")

    def _log(self, msg):
        if self.log:
            self.log(msg)