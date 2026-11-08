# Quiz trắc nghiệm: Databricks & Governance Basics

**Hình thức:** 10 câu hỏi, mỗi câu có bốn lựa chọn A/B/C/D. Chọn một đáp án đúng nhất cho mỗi câu. Câu 7–10 yêu cầu phân tích tình huống.

**Bài đọc nền tảng:** [Databricks & Governance Basics](databricks-governance-basics.md).

## Câu 1

Phát biểu nào mô tả đúng vai trò của workspace, compute và catalog trong Databricks?

A. Workspace thực thi SQL; compute tổ chức bảng; catalog lưu notebook.

B. Workspace tổ chức bảng; compute lập lịch job; catalog cấp tài nguyên thực thi.

C. Workspace tổ chức công việc; compute thực thi câu lệnh; catalog tổ chức tài sản dữ liệu.

D. Workspace quản lý quyền bảng; compute lưu metadata; catalog thực thi notebook.

## Câu 2

Ngoài phân quyền truy cập, nhóm nội dung nào thuộc phạm vi data governance được giới thiệu trong bài?

A. Tăng kích thước compute, mở thêm worker và tối ưu tốc độ CPU.

B. Quản lý metadata, xác định ownership, theo dõi lineage và xem xét audit log.

C. Đổi màu notebook, sắp xếp tab trình duyệt và lựa chọn giao diện.

D. Cài thư viện Python, viết biểu đồ và thay đổi phím tắt của trình soạn thảo.

## Câu 3

Tên bảng `lab_governance.silver.orders_clean` được hiểu đúng theo thứ tự nào?

A. Catalog: orders_clean; schema: silver; table: lab_governance.

B. Catalog: silver; schema: lab_governance; table: orders_clean.

C. Catalog: lab_governance; schema: orders_clean; table: silver.

D. Catalog: lab_governance; schema: silver; table: orders_clean.

## Câu 4

Một user được sử dụng SQL warehouse nhưng chưa được cấp SELECT trên bảng cần đọc. Vì sao chưa thể kết luận user đọc được bảng?

A. Quyền sử dụng compute và quyền truy cập dữ liệu thuộc các phạm vi khác nhau.

B. Quyền sử dụng warehouse tự động cấp SELECT cho mọi bảng.

C. Quyền SELECT chỉ được kiểm tra khi compute đang tắt.

D. Quyền bảng được xác định hoàn toàn bởi tên của warehouse.

## Câu 5

Một analyst đã có USE CATALOG và SELECT nhưng thiếu USE SCHEMA trên schema cha, kể cả qua nhóm hoặc kế thừa. Analyst có đủ quyền đọc bảng không?

A. Có, vì SELECT là điều kiện duy nhất để đọc bảng.

B. Có, vì USE CATALOG luôn bao gồm USE SCHEMA.

C. Chưa; analyst cần có thêm USE SCHEMA trên schema cha.

D. Chưa; chỉ cần thêm MODIFY để thay thế USE SCHEMA.

## Câu 6

Giả sử đã có đủ quyền sử dụng namespace, SELECT cấp trên schema gold khác SELECT chỉ cấp trên bảng gold.daily_sales như thế nào?

A. Grant ở schema chỉ áp dụng cho bảng đã tồn tại tại thời điểm cấp quyền.

B. Grant ở schema có phạm vi rộng hơn, bao gồm các bảng phù hợp hiện có và tạo sau trong schema.

C. Grant ở schema chỉ cho xem metadata, không cho đọc dữ liệu.

D. Grant ở schema tự động cho phép UPDATE và DELETE trên các bảng.

## Vận dụng: phân tích tình huống

## Câu 7

Mai đọc được bảng silver khi chạy notebook bằng tài khoản cá nhân. Khi Mai kích hoạt job, kết quả từng task và danh tính chạy được ghi trong sơ đồ.

![Job đêm · Run as sp_sales. Nạp dữ liệu, bronze.orders_raw, Thành công. Làm sạch, silver.orders_clean, Thành công. Tổng hợp, Đọc silver → ghi gold, Lỗi khi SELECT. sp_sales đã có quyền sử dụng catalog và schema silver, cùng quyền ghi bảng gold đích.](<governance-quiz/Figures/case-7.png>)

Thay đổi nhỏ nhất để sửa đúng lỗi mà vẫn giữ danh tính vận hành là gì?

A. Cấp SELECT trên `silver.orders_clean` cho `sp_sales` rồi chạy lại task bị lỗi.

B. Cấp thêm SELECT trên `silver.orders_clean` cho Mai vì Mai là người bấm chạy.

C. Đổi Run as sang Mai để quyền của job luôn đi theo người đang vận hành.

D. Cấp SELECT ở cấp catalog cho `sp_sales` để job có thể đọc cả các bảng sẽ tạo sau này.

## Câu 8

Sơ đồ mô tả thao tác của job và bảng duy nhất analyst cần đọc.

![Luồng dữ liệu của sp_etl. bronze.orders_raw, Job đọc. silver.orders_clean, Job ghi rồi đọc lại. gold.daily_sales, Job ghi · analyst đọc. Các bảng đã tồn tại. Cả hai bên có quyền compute và chưa có quyền dữ liệu.](<governance-quiz/Figures/case-8.png>)

Phương án nào đáp ứng cả hai luồng công việc và giữ phạm vi quyền hẹp?

A. Cấp SELECT toàn catalog cho cả hai bên, rồi cấp MODIFY ở gold cho `sp_etl`.

B. Cấp `sp_etl` quyền đọc bronze, đọc/ghi silver, ghi gold trên từng bảng; cấp analyst quyền sử dụng catalog, schema gold và SELECT đúng bảng báo cáo; cấp `sp_etl` quyền sử dụng các namespace cần thiết.

C. Cấp quyền tạo bảng ở silver và gold cho `sp_etl`; cấp analyst SELECT trên bảng gold mà không cấp quyền sử dụng schema.

D. Cho analyst đọc bảng silver thay cho gold; dùng quyền chạy job để `sp_etl` tự đọc và ghi các bảng.

## Câu 9

Nhóm cần xác định bước nào làm sai số liệu và danh tính nào thực hiện thao tác liên quan quanh thời điểm đó.

![Luồng cấp dữ liệu cho dashboard. Bronze · đơn hàng gốc, Số đơn gần như không đổi. Silver · orders_clean, Dữ liệu sau làm sạch. Gold · daily_sales, Doanh thu một ngày tăng gấp đôi. Sau lần triển khai tối qua, job báo thành công. Dashboard đọc bảng gold.](<governance-quiz/Figures/case-9.png>)

Thứ tự điều tra nào có khả năng phân biệt lỗi biến đổi với thay đổi dữ liệu ngoài dự kiến?

A. Dùng audit log để tự suy ra công thức tổng hợp rồi sửa dashboard ngay.

B. Xem trạng thái job thành công và chỉ kiểm tra cấu hình SQL warehouse.

C. Chỉ đọc lineage; nếu thấy đủ ba tầng thì kết luận không có lỗi ở pipeline.

D. Dùng lineage xác định nguồn và task liên quan; đối chiếu số dòng, số đơn duy nhất và phép tổng hợp theo từng tầng; xem audit để xác định hoạt động và danh tính trong khoảng thời gian đó.

## Câu 10

Lan vẫn đọc được bảng chi tiết. Sau thay đổi, analyst phải còn đọc được daily_sales và job vẫn cần ghi cả hai bảng.

![Đường cấp quyền đọc của Lan. Lan, Thành viên nhóm analysts. analysts, SELECT ở schema gold. Schema gold, daily_sales · customer_detail. Grant trực tiếp của Lan trên customer_detail đã bị thu hồi. Job ghi qua danh tính riêng.](<governance-quiz/Figures/case-10.png>)

Kế hoạch nào đúng với mục tiêu?

A. Thu hồi USE SCHEMA gold của analyst để chặn bảng chi tiết; giữ nguyên các grant SELECT hiện tại.

B. Chạy thử bằng owner; nếu owner đọc được cả hai bảng thì quyền analyst đã đúng.

C. Cấp SELECT riêng trên `daily_sales` cho `analysts`, gỡ SELECT ở schema và rà các grant khác; thử lại bằng tài khoản analyst và xác nhận job vẫn chạy bằng danh tính riêng.

D. Gỡ quyền ghi của service principal trên `customer_detail` để ngăn Lan đọc bảng.
