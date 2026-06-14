
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
