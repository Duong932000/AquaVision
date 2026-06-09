
import shutil
import kagglehub
from pathlib import Path


def download_kaggle_dataset():
    repo_root = Path(__file__).resolve().parent

    dataset_dir = repo_root / "dataset" / "raw"

    downloaded_path = Path(kagglehub.dataset_download("sachinpatel21/pothole-image-dataset"))
    print(f"[INFO] Dataset downloaded to: {downloaded_path}")

    if dataset_dir.exists():
        shutil.rmtree(dataset_dir)

    shutil.move(str(downloaded_path),str(dataset_dir),)
    print(f"[INFO] Dataset moved to: {dataset_dir}")

if __name__ == "__main__":

    download_kaggle_dataset()