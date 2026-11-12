# Bộ bài học: Databricks & Governance Basics

Bộ tài liệu tách thành lý thuyết, slide, lab, đề trắc nghiệm và lời giải, cùng cách tổ chức với bộ Kafka. Bài đọc, lab, quiz và solution có dự án LaTeX độc lập theo template AIO2026; slide là file PowerPoint dựng từ template trình bày của AIO2026. Mỗi tài liệu đều có bản PDF.

## Các file để đọc và chỉnh sửa

| Tài liệu | Nguồn chỉnh sửa | Dự án / file dựng | PDF |
| --- | --- | --- | --- |
| Bài lý thuyết | [databricks-governance-basics.md](databricks-governance-basics.md) | [governance-basics/main.tex](governance-basics/main.tex) | [Bài đọc](../output/pdf/databricks-governance-basics.pdf) |
| Slide bài giảng | [governance-slides/build_deck.py](governance-slides/build_deck.py) | PowerPoint: [databricks-governance-slides.pptx](../output/databricks-governance-slides.pptx) | [Slide](../output/pdf/databricks-governance-slides.pdf) |
| Lab | [databricks-governance-hands-on.md](databricks-governance-hands-on.md) | [governance-lab/main.tex](governance-lab/main.tex) | [Hướng dẫn lab](../output/pdf/databricks-governance-lab.pdf) |
| Notebook thực hành | [governance-lab/notebooks/](governance-lab/notebooks) | 6 notebook SQL, nhập qua Workspace → Import | — |
| Đề trắc nghiệm | [databricks-governance-quiz.md](databricks-governance-quiz.md) | [governance-quiz/main.tex](governance-quiz/main.tex) | [Đề](../output/pdf/databricks-governance-quiz.pdf) |
| Lời giải | [databricks-governance-solution.md](databricks-governance-solution.md) | [governance-solution/main.tex](governance-solution/main.tex) | [Solution](../output/pdf/databricks-governance-solution.pdf) |

## Nội dung

- **Bài lý thuyết**: Databricks, lakehouse, governance, workspace, compute, Lakeflow Jobs và Run as, metastore/catalog/schema/table, managed table và Delta Lake, metadata, ownership, access control, lineage, audit, principal, quyền và kế thừa, GRANT/REVOKE/SHOW GRANTS.
- **Slide** (25 slide PowerPoint) đi theo bài đọc trong khoảng 60 phút, chia thành bốn section: Databricks và lakehouse; Workspace, compute và jobs; Tổ chức dữ liệu; Governance và phân quyền. Mỗi section mở đầu bằng slide Outline có section đang học được tô đậm và hình minh họa của section đó. Ghi chú cho người dạy nằm trong phần Notes của từng slide, có cả đáp án phần kiểm tra nhanh, nên khi phát cho học viên hãy dùng bản PDF.
- **Lab** dài 90 phút, gồm ba danh tính (quản trị viên, user kỹ sư, user analyst): tạo dữ liệu, cấp quyền theo nhóm, kiểm thử cả thao tác được phép lẫn bị từ chối, REVOKE, job với Run as, rồi dọn dẹp bằng `DROP CATALOG ... CASCADE`. Lab có bảng thời lượng, 8 bằng chứng cần nộp (E1–E8) và 6 câu hỏi (Q1–Q6). Mỗi vai trò có một notebook SQL định dạng Databricks trong `governance-lab/notebooks/` (01 quản trị viên, 02 kỹ sư, 03 analyst, 04 thu hồi quyền, 05 notebook cho job, 06 dọn dẹp); thư mục `governance-basics/lab/` là bản script SQL cũ, giữ lại để tham khảo.
- **Đề** có 10 câu; solution có bảng đáp án và giải thích riêng.

## Trạng thái kiểm chứng lab

Lab **chưa được chạy** trên một workspace Databricks. Các bảng kết quả kỳ vọng tính trực tiếp từ năm đơn hàng mẫu (bronze 5 dòng, silver 3 dòng, gold 2 dòng, tổng 400.00). Hành vi phân quyền và nội dung thông báo lỗi cần được xác nhận bằng hai user thật. Trang giới hạn của Databricks Free Edition (đối chiếu 11/11/2026) không nói rõ có mời thêm user, tạo account group hay chạy `CREATE CATALOG` được hay không, nên cần thử trước ba việc này trên Free Edition hoặc dùng workspace của tổ chức.

## Chỉnh sửa và dựng lại

- **Lý thuyết:** chỉnh `databricks-governance-basics.md` rồi chạy `node databrick/governance-basics/build-from-markdown.mjs`.
- **Lab:** chỉnh `databricks-governance-hands-on.md` rồi chạy `node databrick/governance-lab/build-from-markdown.mjs`. Khối SQL dùng fence `sql` và chỉ chứa ký tự ASCII; script báo lỗi nếu gặp tiếng Việt có dấu trong khối code.
- **Slide:** nội dung, vị trí và ghi chú nằm trong `governance-slides/build_deck.py`; các hàm dùng chung với deck Kafka nằm trong `shared/aio_deck.py` ở thư mục gốc. Chạy `python databrick/governance-slides/build_deck.py` với một Python có `python-pptx`. Nếu sửa trực tiếp trong PowerPoint thì lần chạy script sau sẽ ghi đè các chỉnh sửa đó. Trên trang bìa, nút Data&Code vẫn trỏ tới đường dẫn có sẵn trong template và dòng tác giả đang là “AI VIET NAM – AIO2026”; cần thay bằng thông tin của buổi học.
- **Câu hỏi và lời giải:** chỉnh `governance-quiz/quiz-data.json` rồi chạy `node databrick/governance-quiz/build-quiz.mjs`.

## Biên dịch lại PDF

Máy cần MiKTeX hoặc TeX Live với `pdflatex` trên PATH. Từ thư mục workspace `slaivn`, chạy PowerShell:

```powershell
./databrick/build-pdfs.ps1
```

Script biên dịch bốn PDF (bài đọc, lab, đề, solution) vào `output/pdf/`. Sau đó script dựng lại `output/databricks-governance-slides.pptx` nếu tìm được Python có `python-pptx` (đặt `$env:PPTX_PYTHON` để chỉ định), rồi xuất `databricks-governance-slides.pdf` bằng PowerPoint nếu máy có PowerPoint. Cuối cùng script tạo `output/databricks-governance-latex.zip` gồm các dự án, Markdown, script dựng, module `shared/`, file PowerPoint và ảnh. Khi phát cho học viên, chỉ dùng PDF bài đọc, PDF slide, lab và quiz.
