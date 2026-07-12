# 01 — Claude.ai cơ bản: Giao diện & Cá nhân hóa

## 1. Giao diện và models

Claude.ai có trên web (claude.ai), desktop app (Mac/Windows) và mobile app (iOS/Android). Với gói Pro, bạn được mở khóa model picker đầy đủ và có thể đổi model giữa cuộc hội thoại.

Các dòng model hiện tại (từ mạnh đến nhanh): **Fable/Mythos** (tier mới nhất, mạnh nhất) → **Opus** → **Sonnet** → **Haiku**. Nguyên tắc chọn: task khó, cần suy luận sâu → model mạnh; task đơn giản, cần nhanh → model nhẹ để tiết kiệm hạn mức.

## 2. Bốn lớp cá nhân hóa (rất quan trọng)

### Lớp 1: Personal Preferences (toàn tài khoản)
- Vị trí: **Settings → Profile → "What personal preferences should Claude consider in responses?"**
- Áp dụng cho MỌI cuộc hội thoại
- Nên viết: bạn là ai, làm nghề gì, trình độ, phong cách trả lời mong muốn
- Giữ dưới ~500 từ (nội dung này nạp vào đầu mỗi chat, tốn context)
- Mẹo: mỗi lần Claude làm gì đó khiến bạn khó chịu, thêm một dòng vào preferences để sửa

### Lớp 2: Projects (theo dự án)
- Mỗi Project có **Project Instructions** riêng + **Project Knowledge** (upload file tài liệu)
- Chỉ áp dụng cho các chat trong project đó
- Gói Pro: không giới hạn số project (free chỉ 5)
- Đây là nơi tốt nhất để "dạy" Claude về kiến thức riêng: spec dự án, plan, notes, style guide...
- Chat trong project có thể tham chiếu mọi file trong knowledge base

### Lớp 3: Styles (cách trình bày)
- Điều khiển format và giọng văn: Concise, Explanatory, Formal, hoặc custom
- Có thể tạo style riêng từ mẫu văn của chính bạn (upload writing sample)
- Đổi được giữa cuộc hội thoại

### Lớp 4: Memory (trí nhớ dài hạn)
- **Settings → Capabilities**, bật:
  - "Generate memory from chat history" — Claude ghi nhớ bạn qua thời gian
  - "Search and reference past chats" — hỏi Claude "tìm lại chat về X hôm trước"

Thứ tự nạp: Preferences → Project Instructions → Styles. Thông tin ổn định để ở Preferences; thông tin theo dự án để ở Project; format để ở Styles.

## 3. Settings → Capabilities nên bật

- **Artifacts** — tài liệu/code/app hiển thị ở panel bên
- **AI-powered artifacts** — artifact tự gọi Claude API bên trong (app AI lồng AI)
- **Web search** — tìm kiếm thông tin mới
- **Cloud code execution & file creation** — chạy code, tạo file Word/Excel/PDF/PPT
- **Inline visualizations** — biểu đồ, sơ đồ ngay trong chat
- **Search and reference chats / Memory** — như trên

## 4. Làm việc với file

- Upload: PDF, ảnh, docx, xlsx, csv, code... kéo thả trực tiếp vào chat
- Claude đọc, phân tích, trích xuất, chuyển đổi định dạng
- Độ dài file tính vào hạn mức tin nhắn — file càng dài, tốn quota càng nhanh

## 5. Thao tác hữu ích ít người biết

- Edit lại tin nhắn cũ để "rẽ nhánh" cuộc hội thoại (tiết kiệm quota hơn chat dài)
- Chat quá dài làm tốn quota theo cấp số — nên mở chat mới khi đổi chủ đề
- Thumbs up/down để feedback cho Anthropic
- Keyboard shortcut mở settings: ⌘+Ctrl+, (Mac)

## Link tham khảo

- Personalization: https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features
- Projects: https://support.claude.com (tìm "projects")