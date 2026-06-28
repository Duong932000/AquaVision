
import logging

class UltralyticsUILogHandler(logging.Handler):
    def __init__(self, callback):
        super().__init__()

        self.callback = callback

    def emit(self, record):
        try:
            message = self.format(record)

            message = message.strip()

            if not message:
                return

            if self.callback:
                self.callback("INFO", message)
        except Exception:
            pass
