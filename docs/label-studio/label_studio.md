# LABEL-STUDIO


## Tổng quan

Label studio là công cụ gán nhãn dữ liệu (data labeling) mã nguồn mở đa năng. Nó có thể cho phép người dùng chú thích văn bản, hình ảnh, âm thanh, và video để đào tạo các mô hình AI ‌/, Machine Learning một cách tự động

## Các tính năng

- Đa dạng loại dữ liệu: text, image, audio, video, time-series

- Tự thiết kế UI: cung cấp hệ thống XML đơn giản để tùy chỉnh layout gán nhãn cho phù hợp với từng nhu cầu dự án

- Hỗ trợ ML backend: cho phép kết nối với các mô hình AI có sẵn (SAM - Segment Anything, YOLO) để tự động gán nhãn sơ bộ (pre-label), giúp tăng tốc làm việc lên nhiều lần.

## Ưu điểm

- Xuất dữ liệu: dễ dàng export dataset ra nhiều format: JSON, CSV, COCO, YOLO, TXT để đưa vào quy trình training.

- Self-hosted: cho phép install và run local

## Cài đặt

```text
# Install the package
# into python virtual env
# for fedora linux
python3.11 -m pip install -U label-studio

# launch it
label-studio

# It'll be run on local host at: https://localhost:8080

# Username and password: email nguyendacduong18161006@gmail.com
