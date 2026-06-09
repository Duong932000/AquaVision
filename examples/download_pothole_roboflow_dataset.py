
# Download the pothole detection dataset from Roboflow
# This script uses the Roboflow Python package to download the dataset.
# Content of this script is based on the example provided by Roboflow:
# Just copy paste and run the code below to download the dataset.
# api_key will be changed if the dataset is updated

import shutil
from pathlib import Path
from roboflow import Roboflow


# just change at here if the dataset is updated
API_KEY = "Lh8TTT6NxFVWoqoHVvMW"
WORKSPACE = "dd-1pubd"
PROJECT = "pothole-detection-k6hah"
VERSION = 1
FORMAT = "yolo26"


def download_roboflow_dataset() -> None:

    roboflow_dir = (
        Path(__file__).resolve().parent
        / "dataset"
        / "roboflow"
    )

    roboflow_dir.mkdir(parents=True, exist_ok=True)

    rf = Roboflow(api_key=API_KEY)

    project = rf.workspace(WORKSPACE).project(PROJECT)

    version = project.version(VERSION)

    print("[INFO] Downloading dataset from Roboflow...")

    dataset = version.download(FORMAT)

    downloaded_path = Path(dataset.location)

    print(f"[INFO] Downloaded to: {downloaded_path}")

    target_dir = roboflow_dir / downloaded_path.name

    if target_dir.exists():
        shutil.rmtree(target_dir)

    shutil.move(str(downloaded_path), str(target_dir))

    print(f"[INFO] Dataset moved to: {target_dir}")

    data_yaml = target_dir / "data.yaml"

    if data_yaml.exists():
        print(f"[INFO] data.yaml: {data_yaml}")

if __name__ == "__main__":

    download_roboflow_dataset()

