
class ModelResolver:
    """Resolves a (family, version, size) model selection into a loadable checkpoint name."""

    _YOLO_VERSION_PREFIXES = {
        "YOLO26": "yolo26",
        "YOLO12": "yolo12",
        "YOLO11": "yolo11",
        "YOLOv10": "yolov10",
        "YOLOv9": "yolov9",
        "YOLOv8": "yolov8",
    }

    # Ultralytics only ships "rtdetr-l.pt" / "rtdetr-x.pt" checkpoints; RT-DETRv2
    # weights are not distributed through the ultralytics model zoo.
    _RTDETR_VERSION_PREFIXES = {
        "RT-DETR": "rtdetr",
    }

    @classmethod
    def get_model_name(cls, family, version, size):

        family = (family or "").upper()

        if family == "YOLO":
            return cls._resolve(cls._YOLO_VERSION_PREFIXES, version, f"{{prefix}}{size}.pt")

        if family == "RT-DETR":
            return cls._resolve(cls._RTDETR_VERSION_PREFIXES, version, f"{{prefix}}-{size}.pt")

        raise ValueError(f"Unsupported model family: {family}")

    @staticmethod
    def _resolve(prefixes, version, template):

        prefix = prefixes.get(version)

        if prefix is None:
            raise ValueError(
                f"Unsupported version '{version}' (supported: {', '.join(prefixes)})"
            )

        return template.format(prefix=prefix)
