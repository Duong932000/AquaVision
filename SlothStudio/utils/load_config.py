
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
            = _load_yml_file((_get_root_dir() / "config" / cls._SLOTH_STUDIO_FILE))

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

    @classmethod
    def get_model_families(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["models"]["families"]

    @classmethod
    def get_model_family(cls, family_name):

        cls.initialize()

        return cls._CONFIG_CACHE["models"]["families"][family_name]

    # TRACKER CONFIGURATION -------------------#
    @classmethod
    def get_trackers(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["trackers"]

    @classmethod
    def get_tracker_list(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["trackers"]["available"]

    @classmethod
    def get_default_tracker(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["trackers"]["default"]

    # INFERENCE CONFIGURATION -----------------#
    @classmethod
    def get_inference(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["inference"]

    @classmethod
    def get_inference_source(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["inference"]["source"]

    @classmethod
    def get_inference_models(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["inference"]["models"]

    @classmethod
    def get_inference_tracking(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["inference"]["tracking"]

    @classmethod
    def get_inference_detection(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["inference"]["detection"]

    @classmethod
    def get_inference_output(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["inference"]["output"]

    @classmethod
    def get_inference_runtime(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["inference"]["runtime"]

    # TRAINING CONFIGURATION ------------------#
    @classmethod
    def get_training(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["training"]

    @classmethod
    def get_training_dataset(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["training"]["dataset"]

    @classmethod
    def get_training_models(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["training"]["models"]

    @classmethod
    def get_training_hyperparameters(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["training"]["hyperparameters"]

    @classmethod
    def get_training_validation(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["training"]["validation"]

    @classmethod
    def get_training_export(cls):

        cls.initialize()

        return cls._CONFIG_CACHE["training"]["export"]
