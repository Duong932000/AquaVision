class ValidationProcessor:

    def __init__(self,
                 log_callback=None):

        self.log_callback = log_callback

    def log(self, message):

        if self.log_callback:
            self.log_callback(message)

    def validate(self,
                 model_path):

        self.log(
            f"Validation started: {model_path}\n"
        )

        # future validation logic

        self.log(
            "Validation finished.\n"
        )