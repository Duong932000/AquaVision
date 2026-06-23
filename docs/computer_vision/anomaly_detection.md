
# ANOMALY DETECTION FOR AQUAVISION

## Introduction

### Anomaly Detection là gì?

Anomaly Detection (phát hiện bất thường) là quá trình xác định các mẫu dữ liệu không tuân theo hành vi bình thường đã được quan sát trước đó

Trong AI computer vision cho thủy sản, mục tiêu không phải là phát hiện

Con cá nào bị bệnh?

Mà là: đàn cá có đang có các hành vi bất thuờng hay không? Sớm cảnh báo

Điều này đặc biệt quan trọng vì:

- Phần lớn các bệnh không có biểu hiện hình ảnh rõ ràng ở giai đoạn đầu

- Cá thường biểu hiện bất thường về hành vi trước khi chết

- Chủ trang trại cần cảnh báo sớm thay vì phát hiện sau khi thiệt hại xảy ra

### Vai trò trong AquaVision

AquaVision không hướng tới:

- Fish Identification

- Fish Re-Identification

- Long-term tracking

Mà hướng tới:

- Healthy Fish Monitoring

- Early Warning System

- Feed Optimization

- Operational Decision Support

Do đó Anomaly Detection là một phần trung tâm của hệ thống

### Mối quan hệ giữa YOLO và Anomaly Detection

YOLO là object detection, nó khác với anomaly detection

Anomaly cần:

- Fish count

- Velocity

- Density

- Activity

- Tank Occupancy 

- Surface Ratio

- Motion Trend

Do đó pipeline sẽ là:

    Video
    |
    YOLO
    |
    Feature Extraction
    |
    Anomaly Detection
    |
    Alert

### Các feature quan trọng cho AquaVision

Fish Count: số lượng cá xuất hiện

Average Velocity: Vận tốc trung bình

Density: Mật độ cá trong khung hình

Surface Ratio: Tỉ lệ cá xuất hiện gần mặt nước

Motion Heatmap: Khu vực cá hoạt động nhiều nhất

Occupancy Ratio: Mức độ phân bố trong bể

Feeding Activity Score: Mức độ phản ứng khi cho ăn


## Các thuật toán trong Anomaly Detection

### Isolation Forest

#### Khái niệm:

Isolation Forest là thuật toán phát hiện bất thường dựa trên nguyên lý: Dữ liệu bất thường dễ bị cô lập hơn dữ liệu bình thường

#### Cách hoạt động

Giả sử: 10.000 điểm dữ liệu bình thường

1 điểm dữ liệu bất thường

-> Điểm bất thường sẽ bị tách khỏi dữ liệu rất nhiêu

Ưu điểm:
    - Không cần dữ liệu bất thường
    - Huấn luyện nhanh
    - Triển khai đơn giản
    - Hiệu quả với dữ liệu thống kê

Nhược điểm:
    - Không học được với chuỗi thời gian dài
    - Không hiểu hành vi phức tạp

### LSTM AutoEncoder

#### Khái niệm

LSTM AutoEncoder là AutoEncoder dành cho chuỗi thời gian

#### Kiến trúc

    Time Series
    |
    LSTM Encoder
    |
    Latent Vector
    |
    LSTM Decoder
    |
    Reconstruction

Ví dụ:
Input: 30 phút hoạt động gần nhất

Output: Tái tạo lại chuỗi hoạt động

Nếu sai số lớn: Anomaly

Ưu điểm:
    - Hiểu được xu hướng
    - Hiểu được chu kỳ
    - Thay đổi hành vi theo thời gian
Nhược điểm:
    - Cần nhiều dữ liệu
    - Huấn luyện phức tạp


## So sánh các thuật toán

|Thuật toán	| Dữ liệu bất thường | Time Series | Độ khó
|Isolation Forest |	Không cần | Không | Thấp
|AutoEncoder | Không cần | Hạn chế | Trung bình
|LSTM AutoEncoder | Không cần | Có | Cao
