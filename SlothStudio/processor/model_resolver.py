class ModelResolver:

    @staticmethod
    def get_model_name(family, version, size):

        if family == "YOLO":

            mapping = {
                "YOLO11": f"yolo11{size}.pt",
                "YOLO12": f"yolo12{size}.pt",
                "YOLO26": f"yolo26{size}.pt",
            }

            return mapping[version]

        if family == "RT-DETR":

            mapping = {
                "RT-DETR": f"rtdetr-{size}.pt",
                "RT-DETRv2": f"rtdetrv2-{size}.pt",
            }

            return mapping[version]

        raise RuntimeError(
            f"Unsupported model version: {version}"
        )