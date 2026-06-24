
# RF-DETR (Roboflow Detection Transformer)

RF-DETR là thế hệ DETR realtime mới được phát triển bởi Roboflow với mục tiêu giải quyết bài toán mà cả YOLO và RT-DETR vẫn còn gặp phải

- Accuracy cao nhưng vẫn realtime

- Generalization tốt trên dữ liệu thực tế (không chỉ COCO)

- Fine-tuning hiệu quả trên dataset nhỏ và domain-specific

- Deployment được trên edge device và TensorRT

## Kiến trúc tổng quát

Input Image
      ↓
DINOv2 Backbone
      ↓
Multi-scale Features
      ↓
C2f Projector
      ↓
Shallow DETR Decoder
      ↓
Object Predictions

## RF-DETR cho Fish Tracking

Đối với bài toán top-view Fish Detection

RF-DETR có một số lợi thế:

- Cá chồng lấn nhau

- Cá kích thước thay đổi liên tục

- Điều kiện ánh sáng thay đổi

- Dataset không lớn

