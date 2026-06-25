from abc import ABC, abstractmethod


class BaseTrainer(ABC):

    def __init__(self,
                 config,
                 log_callback=None):

        self.config = config
        self.log_callback = log_callback
        self.stop_requested = False

    def log(self, message):

        if self.log_callback:
            self.log_callback(message)

    def stop(self):

        self.stop_requested = True

    @abstractmethod
    def train(self):
        pass