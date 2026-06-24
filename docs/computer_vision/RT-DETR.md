
# RT-DETR (Real-time Detection Transformer)

## Introduction

RT-DETR là một mô hình Object Detection thuộc họ DETR được phát triển bởi Baidu nhằm giải quyết điểm ý lớn nhất của DETR truyền thống:

- Inference chậm

- Training khó hội tụ

- Không phù hợp cho ứng dụng realtime

RT-DETR là mô hình DETR realtime đầu tiên có thể cạnh trang trực tiếp với YOLO về:

- Speed
- Accuracy
- Deployment

Trong nhiều Benchmark COCO, RT-DETR đạt accuracy cao hơn các YOLO cùng mức latency


## RT-DETR Architecture

High-level architecture

```
Input Image
      ↓
CNN Backbone
      ↓
Multi-scale Features
      ↓
Hybrid Encoder
      ↓
IoU-aware Query Selection
      ↓
Transformer Decoder
      ↓
Object Predictions
```

## Phương pháp

### End-to-end speed of Detectors

NMS

NMS là thuật toán post-processing phổ biến trong các mô hình object detection. Vai trò của NMS là loại bỏ các box
dự đoán bị chồng chéo lên nhau.
Hai hyperparameter đựoc yêu cần trong NMS là score threshold và IoU threshold.