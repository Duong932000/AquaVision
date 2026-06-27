
import os
import yaml
from pathlib import Path

def _get_root_dir():

    return Path(os.getenv("ROOT_DIR", ".")).resolve()

def _load_yml_file(file_path):

    if not file_path.exists():
        raise FileNotFoundError(f"File not found at: {file_path}")
    
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


class InitialConfigLoader:

    _CONFIG_CACHE = None
    _SLOTH_STUDIO_FILE = "slothstudio.yml"

    @classmethod
    def initialize(cls):

        if cls._CONFIG_CACHE is not None:
            return

        cls._CONFIG_CACHE \
            = _load_yml_file((_get_root_dir() / "SlothStudio" / "config" / cls._SLOTH_STUDIO_FILE))

    @classmethod
    def reload(cls):

        cls._CONFIG_CACHE = None

        cls.initialize()

    @classmethod
    def get_all(cls):

        cls.initialize()

        return cls._CONFIG_CACHE

    # APPLICATION CONFIGURATION ---------------#
    @classmethod
    def get_application(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["application"]

    # MODEL CONFIGURATION ---------------------#
    @classmethod
    def get_models(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["models"]

    # TRACKER CONFIGURATION -------------------#
    @classmethod
    def get_trackers(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["trackers"]

    # INFERENCE CONFIGURATION -----------------#
    @classmethod
    def get_inference(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["inference"]

    # TRAINING CONFIGURATION ------------------#
    @classmethod
    def get_training(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["training"]

