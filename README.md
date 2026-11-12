# Databricks & Governance Basics

Workspace, compute, Lakeflow Jobs, Unity Catalog và quyền truy cập dữ liệu. Bộ tài liệu tiếng Việt dùng ví dụ đơn hàng.

| Tài liệu | Nguồn | Bản phát hành |
| --- | --- | --- |
| Lý thuyết | [Bài đọc](databrick/databricks-governance-basics.md) | [PDF](output/pdf/databricks-governance-basics.pdf) |
| Slide bài giảng | [Script dựng slide](databrick/governance-slides/build_deck.py) | [PowerPoint](output/databricks-governance-slides.pptx) · [PDF](output/pdf/databricks-governance-slides.pdf) |
| Lab 90 phút | [Hướng dẫn](databrick/databricks-governance-hands-on.md) · [Notebook thực hành](databrick/governance-lab/notebooks/) | [PDF](output/pdf/databricks-governance-lab.pdf) |
| Quiz | [Đề có sơ đồ](databrick/databricks-governance-quiz.md) | [PDF](output/pdf/databricks-governance-quiz.pdf) |
| Lời giải | [Đáp án và giải thích](databrick/databricks-governance-solution.md) | [PDF](output/pdf/databricks-governance-solution.pdf) |

[Gói nguồn](output/databricks-governance-latex.zip) · [Template AIO2026](Template%20Reading/template.tex)

Lab gồm ba danh tính (quản trị viên, user kỹ sư, user analyst), có bảng thời lượng, 8 bằng chứng cần nộp và 6 câu hỏi. Mỗi vai trò có một notebook SQL định dạng Databricks trong [databrick/governance-lab/notebooks/](databrick/governance-lab/notebooks/); nhập vào workspace qua Workspace → Import. Lab chưa được chạy trên một workspace cụ thể: các bảng “Kết quả kỳ vọng” tính trực tiếp từ năm đơn hàng mẫu, còn hành vi phân quyền cần được xác nhận bằng hai user thật. Slide PowerPoint có ghi chú cho người dạy trong phần Notes (gồm đáp án phần kiểm tra nhanh); khi phát cho học viên, dùng bản PDF.

Các dự án LaTeX, ảnh và tài liệu nguồn nằm trong thư mục [databrick/](databrick/). Mở file main.tex trong từng dự án và dùng pdflatex để biên dịch. Khi cần tạo lại nội dung từ Markdown, cài marked bằng lệnh `npm install --no-save marked` rồi chạy script mjs tương ứng. Script dựng slide cần Python có `python-pptx` và file template trình bày AIO2026 (`Template Format trình bày.pptx`) đặt ở thư mục gốc; template này không nằm trong repo.

[Hướng dẫn dựng lại bộ Databricks](databrick/README.md) · [Script SQL cũ cho hands-on](databrick/governance-basics/lab/)
