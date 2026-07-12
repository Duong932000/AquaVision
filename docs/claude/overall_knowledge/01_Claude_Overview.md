# 01 — Tổng quan hệ sinh thái Claude & Lộ trình học

> Cập nhật: Tháng 7/2026. Claude thay đổi rất nhanh — luôn đối chiếu với tài liệu chính thức khi có nghi ngờ.

## Hệ sinh thái Claude gồm những gì?

| Sản phẩm | Là gì | Dùng khi nào |
|---|---|---|
| **Claude.ai** (web/desktop/mobile) | Giao diện chat chính | Hỏi đáp, viết lách, nghiên cứu, phân tích file |
| **Claude Code** | Agent lập trình chạy trong terminal, IDE, desktop app, web | Code, refactor, debug, tự động hóa dev workflow |
| **Claude Cowork** | App desktop cho công việc tri thức (non-dev) | Task nhiều bước với file, research, phân tích |
| **Claude in Chrome / Excel / PowerPoint** | Agent trong trình duyệt / bảng tính / slide | Thao tác web, xử lý spreadsheet, làm slide |
| **Claude API / Console** | Truy cập lập trình qua API | Build ứng dụng riêng (tính phí riêng, KHÔNG nằm trong gói Pro) |

**Điểm quan trọng nhất với Pro plan:** một subscription duy nhất dùng được cả Claude.ai (web/desktop/mobile) VÀ Claude Code (terminal + IDE), chia sẻ chung hạn mức sử dụng.

## Lộ trình học đề xuất (4 tuần)

### Tuần 1 — Nền tảng Claude.ai
- Đọc file `01-claude-ai-co-ban.md`
- Set up Personal Preferences, bật các capabilities trong Settings
- Tạo Project đầu tiên, upload knowledge files
- Thực hành: dùng Artifacts, web search, upload file phân tích

### Tuần 2 — Khai thác tính năng mạnh
- Đọc file `03-tinh-nang-manh-claude-ai.md`
- Thực hành Research mode cho một chủ đề bạn quan tâm
- Tạo file Word/Excel/PDF bằng file creation
- Kết nối 1-2 connector (Google Drive, GitHub...)

### Tuần 3 — Claude Code cơ bản
- Đọc file `04-claude-code-co-ban.md`
- Cài đặt, đăng nhập bằng tài khoản Pro
- Chạy `/init` trên một repo thật, học cách viết CLAUDE.md
- Thực hành Plan Mode, checkpoints, các slash command cốt lõi

### Tuần 4 — Claude Code nâng cao
- Đọc file `05-claude-code-nang-cao.md`
- Viết skill đầu tiên, thử subagent, thêm 1 MCP server
- Đọc file `06-prompting-hieu-qua.md` và áp dụng xuyên suốt

## Danh sách file trong bộ tài liệu

1. `00-tong-quan-va-lo-trinh.md` — file này
2. `01-claude-ai-co-ban.md` — giao diện, cá nhân hóa, Projects, Styles, Memory
3. `02-pro-plan.md` — gói Pro có gì, hạn mức, cách tối ưu
4. `03-tinh-nang-manh-claude-ai.md` — Artifacts, Research, file creation, connectors, Cowork
5. `04-claude-code-co-ban.md` — cài đặt, CLAUDE.md, plan mode, slash commands
6. `05-claude-code-nang-cao.md` — Skills, Subagents, Hooks, MCP, Plugins
7. `06-prompting-hieu-qua.md` — kỹ thuật prompt để Claude làm việc tốt nhất

## Link tài liệu gốc quan trọng

- Claude.ai Help Center: https://support.claude.com
- Claude Code docs: https://code.claude.com/docs
- Claude API docs: https://docs.claude.com
- Prompt engineering: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview
- Tin sản phẩm: https://www.anthropic.com/news