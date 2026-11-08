# Solution: Databricks & Governance Basics

**Đề trắc nghiệm:** [Quiz ôn tập](databricks-governance-quiz.md).

## Bảng đáp án

| Câu | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Đáp án | C | B | D | A | C | B | A | B | D | C |

## Giải thích

### Câu 1 — Đáp án C

**Workspace, compute và catalog.** Workspace tổ chức công việc; compute thực thi câu lệnh; catalog tổ chức tài sản dữ liệu.

Workspace là môi trường tổ chức notebook, file và công việc. Compute cung cấp tài nguyên thực thi; catalog nhóm các tài sản trong namespace dữ liệu. Ba thành phần có các trách nhiệm khác nhau, nên không thể suy ra quyền dữ liệu chỉ từ vị trí notebook hoặc compute đang dùng.

### Câu 2 — Đáp án B

**Phạm vi của data governance.** Quản lý metadata, xác định ownership, theo dõi lineage và xem xét audit log.

Governance còn liên quan đến việc hiểu dữ liệu đang có, ai chịu trách nhiệm, dữ liệu bắt nguồn từ đâu và các hoạt động sử dụng đã diễn ra. Metadata, ownership, lineage và audit hỗ trợ những nhu cầu này. Các lựa chọn còn lại tập trung vào tài nguyên tính toán hoặc công cụ làm việc.

### Câu 3 — Đáp án D

**Namespace ba cấp.** Catalog: lab_governance; schema: silver; table: orders_clean.

Namespace của bảng có dạng `catalog.schema.table`. Do đó, lab_governance là catalog, silver là schema và orders_clean là table. Thứ tự này giúp xác định đúng đối tượng ngay cả khi có nhiều bảng trùng tên trong các schema khác nhau.

### Câu 4 — Đáp án A

**Quyền sử dụng compute và quyền dữ liệu.** Quyền sử dụng compute và quyền truy cập dữ liệu thuộc các phạm vi khác nhau.

Được sử dụng warehouse cho phép user dùng tài nguyên thực thi, nhưng không tự cấp quyền đọc mọi bảng. Truy cập bảng vẫn phụ thuộc quyền dữ liệu và các quyền sử dụng namespace cha. Vì thế, cần kiểm tra cả hai phạm vi khi chẩn đoán lỗi truy vấn.

### Câu 5 — Đáp án C

**Điều kiện đọc bảng Unity Catalog.** Chưa; analyst cần có thêm USE SCHEMA trên schema cha.

Truy vấn đọc bảng cần quyền sử dụng catalog, quyền sử dụng schema cha và SELECT tương ứng. Giả thiết đã loại trừ đường nhận USE SCHEMA qua nhóm hoặc kế thừa, nên quyền này còn thiếu. MODIFY phục vụ thay đổi dữ liệu và không thay thế USE SCHEMA.

### Câu 6 — Đáp án B

**Phạm vi và kế thừa quyền.** Grant ở schema có phạm vi rộng hơn, bao gồm các bảng phù hợp hiện có và tạo sau trong schema.

Trong privilege model được trình bày, quyền dữ liệu cấp ở schema có thể kế thừa xuống các đối tượng con tương ứng, gồm cả bảng tạo sau. Grant SELECT ở một bảng có phạm vi hẹp hơn. SELECT không tự cấp các quyền thay đổi dữ liệu như UPDATE hoặc DELETE.

### Câu 7 — Đáp án A

**Chẩn đoán lỗi Run as.** Cấp SELECT trên `silver.orders_clean` cho `sp_sales` rồi chạy lại task bị lỗi.

Lỗi xảy ra khi `sp_sales` đọc đúng một bảng, nên cấp SELECT trên bảng đó. B cấp quyền cho sai danh tính. C đổi mô hình vận hành dù không cần; D mở phạm vi quyền ra ngoài bảng cần đọc.

### Câu 8 — Đáp án B

**Thiết kế quyền theo đường đọc và ghi.** Cấp `sp_etl` quyền đọc bronze, đọc/ghi silver, ghi gold trên từng bảng; cấp analyst quyền sử dụng catalog, schema gold và SELECT đúng bảng báo cáo; cấp `sp_etl` quyền sử dụng các namespace cần thiết.

B đi theo từng cạnh đọc/ghi của pipeline và cấp quyền sử dụng các cấp cha. A vừa mở rộng quyền đọc của analyst vừa thiếu quyền ghi silver. C nhầm quyền tạo bảng với quyền thao tác trên bảng hiện có và thiếu quyền namespace cho analyst. D đổi nguồn báo cáo và nhầm quyền chạy job với quyền dữ liệu.

### Câu 9 — Đáp án D

**Điều tra sai lệch doanh thu.** Dùng lineage xác định nguồn và task liên quan; đối chiếu số dòng, số đơn duy nhất và phép tổng hợp theo từng tầng; xem audit để xác định hoạt động và danh tính trong khoảng thời gian đó.

Lineage định hướng nơi kiểm tra; số liệu theo từng tầng giúp tìm chỗ nhân bản hoặc tổng hợp sai; audit cung cấp dấu vết thao tác tùy sự kiện. A dùng audit sai mục đích. B không kiểm tra tính đúng của dữ liệu. C nhầm việc có đường phụ thuộc với bằng chứng phép biến đổi đúng.

### Câu 10 — Đáp án C

**Thu hẹp quyền mà không làm gián đoạn job.** Cấp SELECT riêng trên `daily_sales` cho `analysts`, gỡ SELECT ở schema và rà các grant khác; thử lại bằng tài khoản analyst và xác nhận job vẫn chạy bằng danh tính riêng.

Grant cấp schema là một đường cấp quyền còn hiệu lực. C chuyển quyền đọc cần giữ xuống đúng bảng, gỡ đường cấp rộng và kiểm tra bằng đúng danh tính. A làm mất cả đường đọc báo cáo. B dùng owner nên không phản ánh quyền analyst. D tác động nhầm quyền ghi của job, không gỡ quyền đọc của Lan.
