from ultralytics import YOLO

def main():

    # Load pretrained YOLO11 Large
    model = YOLO("yolo11n.pt")

    results = model.train(
        data="Koi_dataset.yolov11/data.yaml",
        epochs=60,
        imgsz=1280,
        batch=8,
        device=0,
        workers=8,

        project="runs",
        name="koi_detection",

        pretrained=True,
        cache=True,

        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,

        degrees=10,
        translate=0.1,
        scale=0.5,
        shear=2.0,

        fliplr=0.5,
        mosaic=1.0,
        mixup=0.1,

        patience=20,

        save=True,
        save_period=10,
    )

    print(results)

if __name__ == "__main__":
    main()