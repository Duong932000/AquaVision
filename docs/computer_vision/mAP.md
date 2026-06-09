# MEAN AVERAGE PRECISION (mAP) for AquaVision


## mAP là gì?

Mean Average Precision (mAP) là metric phổ biến nhất để đánh giá chất lượng của mô hình Object Detection

mAP đo lường đồng thời:

- Model có phát hiện đúng đối tượng hay không (Classification)
- Bounding Box có chính xác hay không (Localization)

Giá trị:
```text
0.0 --> Rất kém

1.0 --> Hoàn hảo
```

Trong thực tế thường biểu diễn theo phần trăm

```text
mAP = 0.85 = 85%  
```


## Các metric quan trọng


### IoU (Intersection over Union)

Đo mức độ chồng lấp giữa:

- Ground Truth Box

- Predicted Box

```text
IoU = Intersection /‌ Union
```

Ví dụ:

```text
IoU = 1.0   --> Trùng hoàn toàn
IoU = 0.7   --> Khá chính xác
IoU = 0.3   --> Lệch nhiều 
```


### Precision

Trong số các đối tượng model phát hiện bao nhiêu là đúng

```text
Precision = TP ‌/ (TP + FP)
```

Precision cao:

- Ít nhận diện nhầm

- Ít False Positive


### Recall

Trong số các đối tượng thực tế tồn tại thì model tìm được bao nhiêu

```text
Recall = TP ‌/ (TP + FN)
```

Recall cao:

- Ít bỏ sót cá

- Ít False Negative


### AP (Average Precision)

AP là diện tích dưới đường cong Precision - Recall

AP càng cao -> Model càng tốt

### Các loại mAP phổ biến

#### mAP50

```text
Điều kiện:

IoU >= 0.5

thì detection được tính là đúng

Đây là metric tương đối dễ đạt được điểm cao
```

#### mAP50-95

```text
Được tính trên nhiều mức IoU

0.50
0.55
0.60
...
0.95

Sau đó lấy trung bình

Metric này nghiêm ngặt hơn và phản ánh chất lượng bounding box chính xác hơn.
```


## Ví dụ trong AquaVision

### Dataset

```text
Class: Fish
Model: YOLO11
Tracker: ByteTrack

Ground Truth:

Video có 100 con cá xuất hiện

Model phát hiện:

- 95 con đúng

- 5 con nhầm

- 10 con bị bỏ sót

--> Kết quả:

+ TP (True Positive):   95

+ FP (False Positive):  5

+ FN (False Negative):  10

--> Precision = TP ‌/ (TP + FP) = 95 ‌/ (95 + 5) = 95%

--> Recall = TP ‌/ (TP + FN) = 95 / (95 + 10) = 90.5%

Nếu Bounding Box đủ chính xác:

+ mAP50 = 95%
+ mAP50-95 = 80%

--> Đây là mức tốt cho bài toán Fish Detection
```


## Mục tiêu đề xuất cho AquaVision

Metric | Target
Precision | > 90%
Recall | > 85%
mAP | > 90%
mAP50-95 | >80%
