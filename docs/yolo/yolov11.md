# YOLO (YOU ONLY LOOK ONCE) RESEARCH NOTES

## Mục tiêu

Nghiên cứu và giải thích lý do tại sao AquaVision chọn YOLOv11 làm mô hình object tracking chính cho hệ thống

Trong kiến trúc AquaVision, YOLOv11 chịu trách nhiệm phát hiện cá trên từng frame trứoc khi chuyển kết quả sang ByteTrack để thực hiện tracking

```text
Video Frame
    ↓
YOLO11
    ↓
Bounding Boxes
    ↓
ByteTrack
    ↓
Fish Trajectories
```


## Vai trò của Object Detection trong AquaVision

Có một thực tế:

- ByteTrack không phát hiện được cá

- ByteTrack chỉ theo dõi các đối tượng đã được detector phát hiện

Do đó chất lượng tracking phụ thuộc trực tiếp vào detection


## Tại sao YOLOv11

AquaVision cần một detector đáp ứng:

- Độ chính xác cao: môi trường nuôi cá có nhiều thách thức:
    + Mặt nứoc phản chiếu
    + Bọt khí
    + Cá chồng lấp lên nhau
    + Cá bơi thành đàn
    + Ánh sáng thay đổi
Do đó detector cần làm việc tốt trong các điều kiện này

- Real-time: 20 bể nuôi, 1 camera 1 bể, 20 luồng RTSP. Do đó detector phải đủ nhanh để xử lý nhiều camera

- Dễ triển khai: mô hình cần hỗ trợ Docker, ONNX, TensorRT, CUDA, Linux mà không cần custom phức tạp.

- Cộng đồng lớn: có tài liệu, có roadmap, giảm rủi ro kỹ thuật trong quá trình develop


## Các phiên bản YOLOv11

```text
- YOLO11n (nano)        : Ưu điểm: nhanh nhất, nhẹ nhất. Nhược điểm: accuracy thấp
- YOLO11s (small)       : Ưu điểm: cân bằng, GPU yêu cầu thấp
- YOLO11m (medium)      : Ưu điểm: accuracy cao hơn. Nhược điểm: tốn GPU hơn.
- YOLO11l (large)       : Ưu điểm: accuracy rất cao. Nhược điểm: tốn GPU hơn.
- YOLO11x (extra large) : Ưu điểm: accuracy rất cao. Nhược điểm: tốn GPU hơn.
```
