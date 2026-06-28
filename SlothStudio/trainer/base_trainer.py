
from abc import ABC, abstractmethod
import threading

class BaseTrainer(ABC):
    def __init__(self, config, log_callback=None):

        self.config = config

        self.log_callback = log_callback
        
        self.stop_event = threading.Event()

        self.model = None

    def log(self, level, message):

        if self.log_callback:
            self.log_callback(level, message)

    def stop(self):

        self.stop_event.set()

        self.log("WARNING", "Stopping training ...")

    @abstractmethod
    def train(self):
        pass