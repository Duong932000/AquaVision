# AQUAVISION ROADMAP


## Tầm nhìn

AquaVision là nền tảng AI Computer Vision dành cho hệ thống nuôi thủy sản tuần hoàn (RAS), giúp người nuôi giám sát sức khỏe đàn cá theo thời gian thực, phát hiện sớm các dấu hiệu bất thường và hỗ trợ ra quyết định vận hành

Mục tiêu cuối cùng của hệ thống không phải là Monitoring System mà là:
```text
- Giảm tỷ lệ cá chết
- Phát hiện sớm các nguy cơ
- Tối ưu hiệu quả sử dụng thức ăn
- Nâng cao sức khỏe đàn cá
- Giảm chi phí vận hành
- Tiến tới mô hình trang trại thông minh tự động hóa
```

## Nguyên tắc phát triển

AquaVision được xây dựng theo thứ tự ưu tiên của giá trị kinh doanh

Không phát triển theo hướng:
    - Segmentation
    - Tracking
    - Re-Identification

Mà phát triển theo hướng:
    - Giữ cá khỏe
    - Tối ưu tăng trưởng
    - Tối ưu lợi nhuận
    - Tự động hóa vận hành


## Chiến lược phát triển

### Phase 0 - Nền tảng dữ liệu

- Mục tiêu: Xây dựng hạ tầng dữ liệu phục vụ toàn bộ hệ thống

- Chức năng:
    Thu thập dữ liệu
        + Streamning detection được từ youtube
        + Thu thập video từ camera thực tế
        + Quản lý metadata

    Trích xuất dữ liệu:
        + Video -> Frame
        + Sampling theo FPS tùy chỉnh

    Gán nhãn dữ liệu:
        + Bounding Box
        + Dataset Versioning

    Pipeline huấn luyện
        + YOLO training
        + Validation
        + Experiment Tracking

    Pipeline triển khai:
        + Export Model
        + Inference
        + Edge deployment

- Kết quả:
    Dataset chuẩn hóa
    Mô hình nhận diện cá
    Quy trình AI hoàn chỉnh


### Phase 1 - Giám sát hoạt động cơ bản

- Mục tiêu: xác định đàn cá có hoạt động bình thường hay không/

- Chức năng:
    Fish Detection: Phát hiện cá trong khung hình

    Basic Tracking:
        + Tracing ngắn hạn phục vụ phân tích hành vi
        + Không theo dõi từng cá thể lâu dài

    Tank Activity Index:
        + Mức độ hoạt động trung bình
        + Mật độ cá xuất hiện
        + Cường độ vận động

    Historical Activity Trend:
        So sánh theo: giờ, ngày, tuần, tháng

    Cảnh báo:
        + Hoạt động giảm mạnh
        + Không phát hiện chuyển động (tùy loại cá và thời điểm)
        + Mật độ xuất hiện bất thường


### Phase 2 - Phát hiện hành vi bất thường

- Mục tiêu: Phát hiện dấu hiệu bất thường trước khi cá chết

- Chức năng:
    Activity Anomaly Detection:
        + Hoạt động giảm bất thường
        + Hoạt động tăng bất thường
        + Hoảng loạn tập thể
    
    Phát hiện cá tập trung gần mặt nước (tùy loài)
        + Nguyên nhận có thể: thiếu oxy hòa tan, chất lượng nước suy giảm

    Phát hiện cá tụ tập tại một khu vực bất thường
        + Nguyên nhân có thể: stress, vùng nước xấu, dòng chảy không đồng đều

    Phát hiện bơi vòng tròn, đổi hướng liên tục

- Kết quả: đây là giai đoạn quan trọng, cần đưa ra các cảnh bảo với các tag như [WARNING], [CRITICAL] để sớm cảnh bảo cho chủ trang trại


### Phase 3 - Hệ thống AI Computer Vision hỗ trợ cho ăn tối ưu

- Mục tiêu: tối ưu hiệu quả sử dụng thức ăn

- Chức năng:
    Đánh giá phản ứng của cá khi cho ăn
    Đo thời gian đàn cá còn phản ứng với thức ăn
    Đánh dấu và so sánh theo từng ngày cho ăn

- Kết quả: cảnh bảo giảm khẩu phần, tăng khẩu phần, nghi ngờ cá bệnh


### Phase 4 - Phát hiện cá chết

- Mục tiêu: Phát hiện cá chết nhanh nhất có thể

- Chức năng:
    Phát hiện cá nổi bất động
    Cá chìm bất động
    Cá có tư thế bất thường

- Kết quả: Gửi cảnh báo ngay lập tức để giảm rủi ro lây nhiễm bệnh
