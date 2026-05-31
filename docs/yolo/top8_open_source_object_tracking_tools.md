# TOP 8 OPEN SOURCE OBJECT TRACKING TOOLS - ALGORITHMS COMPARED


## Overview

Khi một chiếc xe vượt đèn đỏ và vé phạt tự động được gửi về tài xế, hoặc khi một cầu thủ bóng đá dẫn bóng trên sân và camera theo sát pha bóng một cách mượt mà. Chính là do có sự can thiệp của Computer Vision, một lĩnh vực của AI cho phép máy tính nhìn, diễn giải và hiểu thông tin hình ảnh từ thế giới thực.

Trong lĩnh vực Computer Vision, một trong những tác vụ then chốt đằng sau các ứng dụng này là Object Tracking. Cho phép theo dõi khi di chuyển, chồng lấp lên nhau hoặc thay đổi hướng.


## Definition

Object Tracking là gì?

Object Tracking là quá trình theo dõi đối tượng khi nó di chuyển qua các khung hình của video và duy trì tính nhất quán về định danh của nó từ khung hình này sang khung hình tiếp theo.

Trong nhiều hệ thống, quá trình này bắt đầu bằng Object Detection, giúp tìm kiếm và dán nhãn các đối tượng như người, phương tiện, hoặc biển báo giao thông trong mỗi khung hình. Sau đó, khi các đối tượng thay đổi vị trí, xuất hiện, biến mất, hoặc chồng lấp, hệ thống tracking sẽ liên kết các kết quả detection qua các khung hình để biết đối tượng nào là đối tượng và vị trí của từng đối tượng theo thời gian thực.

![Object-Tracking](assets/object_tracking.png)


## Classification

Có 2 loại tracking phổ biến:

- SOT (Single Object Tracking): tập trung vào 1 đối tượng chính

- MOT (Multi-object tracking): theo dõi nhiều đối tượng cùng lúc và gán nhãn cho mỗi đối tượng ID duy nhất.

Bất cả loại tracking nào, đều dựa vào 3 điểm cốt lõi:

- Detector: để tìm kiếm đối tượng trong khung hình.

- Motion Model: để dự đoán hướng di chuyển khả thi của đối tượng

- Matching step: để kết nối các detection mới với các đối tượng đã được theo dõi trước đó.


## Top 8

- [1] Ultralytics YOLO models và Ultralytic Python Package:
    + Hỗ trợ hàng loạt các tác vụ tị giác bao gồm: object detection, instance segmentation, pose estimation, object tracking. 
    + Bản thân các mô hình này không theo dõi đối tượng trên nhiều khung hình. Thay vào đó, Ultralytics Python Package giúp đơn giản hóa việc chạy và triển khai các mô hình Ultralytics YOLO, giúp việc tracking trở nên khả thi bằng cách kết hợp kết quả detection từng khung hình của YOLO với các thuật toán multi-object tracking chuyên dụng như BoT-SORT và ByteTrack.

![Ultralytics](assets/ultralytics.png)


- [2] OpenCV Trackers:
    + Là một thư viện computer vision đồ sộ bao gồm tập hợp các thuật toán object tracking từ năm 1999 đến nay.
    + Dù không đựoc mạnh mẽ như các hệ thống tracking dựa trên Deep Learning hiện đại, chúng vẫn đựoc sử dụng vì nhẹ, nhanh và dễ triển khai.


- [3] ByteTrack:
    + Là một trong những thuật toán phổ biến cho MOT mã nguồn mở. Thay vì chỉ khớp các kết quả detection mà mô hình rất tự tin, nó cũng tận dụng các kết quả detection có độ tin cậy thấp mà nhiều hệ thống thường bỏ qua.
    + Điều này giúp nó tiếp tục theo dõi các đối tượng khó nhìn thấy trong thời gian ngắn, chẳng hạn như chúng bị che khuất một phần, ở xa hoặc di chuyển nhanh.
    + Điểm sáng là ByteTrack đã được tích hợp vào trong Ultralytics YOLO, nên việc kích hoạt qua Ultralytic Python Package rất dễ dàng.

![ByteTrack Algorithm](assets/ByteTrack_algorithm.png)


- [4] DeepSORT
    + DeepSORT là viết tắt của Deep simple Online and Real-time Tracking, tương tự như ByteTrack, SORT tuân theo cách tiếp cận tracking-by-detection, tuy nhiên DeepSORT dựa vào Kalman filter, một mô hình toán học ước tính vị trí tương lai của đối tượng dựa treo chuyển động trong quá khứ, để dự đoán hướng di chuyển tiếp theo của từng đối tượng.
    + Tuy nhiên, hiện nay DeepSORT được coi như một baseline cổ điển, và các phương pháp tracking mới hơn đạt hiệu suất tốt hơn.

![DeepSORT Algorithm](assets/DeepSORT_algorithm.png)


- [5] Norfair
    + Là một thư viện tracking nhẹ đựoc thiết kế để linh hoạt, thay vì ép buộc bạn vào một pipeline tracking cố định. No cho phép khả năng thêm tracking trên hầu hết detector, miễn đầu ra của detector có thể đựoc biểu diễn dưới dạng các điểm, như tâm bbox, keypoints, ...
    + Norfair thường được sử dụng trong robot, phân tích chuyển động thể thao, điều hướng drone và các ứng dụng dựa nhiều vào các điểm landmark hoặc keypoints của cơ thể.

- [6] MMTracking
    + Đựa phát triển từ nhóm OpenMMLab, là một thư viện linh hoạt để phát triển và thử nghiệm các hệ thống tracking.
    + Ít được sử dụng rộng rãi ở production

- [7] FairMOT
    + FairMOT là một framework multi-object traking đựoc thiết kế để theo dõi nhiều đối tượng cùng lúc. Không giống như các pipeline tracking-by-detection truyền thống chạy detection trước rồi mới liên kết các đối tượng qua khung hình như một bứoc riêng biệt, FairMOT học việc detection và re-indetification cùng lúc trong một mạng duy nhất.

![FairMOT Algorithm](assets/FairMOT_algorithm.png)


- [8] SlamMask: Là một phương pháp single-object tracking đi xa hơn nhiều trình theo dõi khác bằng cách tạo ra một segmentation mask cùng bbox. Không chỉ dừng lại ở việc vẽ khung chữ nhật, nó cùng phác thảo hình dạng của đối tượng theo dõi ở mức pixel.

![SlamMask](assets/SlamMask.png)


## Key factor in choosing an Object Tracking Tools

Cần theo dõi các tiêu chí:

- Accuracy: điều quan trọng nhất trong các trường hợp cho tracking cảnh đông đúc, nơi hệ thống cần duy trì ID ổn đỉnh khi bị chồng lấp, che khuất hoặc di chuyển nhanh

- Speed: Đối với các ứng dụng thời gian thực như robot, giám sát giao thông và phân tích thể thao, khả năng phản hồi có thể quan trọng hơn độ chính xác hoàn hảo.

- Ease of integration: cần có yếu tố plug-and-play để dễ dàng triển khai.

- Deployment Constrainst: môi trừong mục tiêu, chẳng hạn như có GPU hay không, edge AI thì có thể lựa chọn loại tracking nào.

- Scalability: Nếu hệ thống cần theo dõi cùng lúc nhiều đối tượng hoặc xử lý nhiều luồng video, tracker cần phải mở rộng quy mô một cách hiệu quả mà không bị giảm hiệu suất đáng kể.
