
import os
import cv2


class TrainingProcessor:
    def __init__(self, config, log_callback, progress_callback):

        self.training_cfg = config
        