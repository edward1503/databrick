# Hands-on: Databricks & Governance Basics

*Tổ chức catalog, schema, table và kiểm tra quyền truy cập bằng từng danh tính*

**Bài đọc nền tảng:** [Databricks & Governance Basics](databricks-governance-basics.md).

**Mục tiêu:** sau buổi lab, học viên tạo được cấu trúc catalog, schema và bảng đơn hàng, chuyển một ma trận quyền thành các câu `GRANT` theo nhóm, rồi kiểm thử bằng đúng danh tính cả thao tác được phép lẫn bị từ chối. Học viên quan sát được việc thu hồi quyền và danh tính Run as của một job.

**Kiến thức cần có:** SQL cơ bản và các khái niệm workspace, compute, jobs, namespace, principal, grant trong bài đọc nền tảng.

> **Trạng thái:** lab chưa được chạy trên một workspace cụ thể. Các bảng “Kết quả kỳ vọng” được tính trực tiếp từ năm đơn hàng mẫu của lab, không phải ảnh chụp lượt chạy. Hành vi phân quyền (bị từ chối hay không, nội dung thông báo lỗi) chỉ được xác nhận khi chạy bằng hai user thật; ghi lại nguyên văn kết quả bạn nhận được.

## 1. Thiết kế buổi lab

### 1.1. Thời lượng và liên hệ với bài lý thuyết

Buổi lab dài **90 phút**. Các bước 1–3 do quản trị viên lab chuẩn bị; trong lớp, giảng viên có thể làm trước hoặc trình diễn để dành thời gian cho phần kiểm thử.

| Phần | Nội dung | Thời gian | Mục lý thuyết |
| --- | --- | --- | --- |
| 2 | Kiểm tra môi trường, danh tính, thiết kế quyền | 10 phút | 4.2, 7.1, 7.2 |
| 3 | Tạo catalog, schema và ba bảng đơn hàng | 15 phút | 5.1–5.5 |
| 4 | Cấp quyền theo nhóm, xem grant | 10 phút | 7.3–7.5 |
| 5 | Kiểm thử bằng user kỹ sư | 15 phút | 7.3, 7.4 |
| 6 | Kiểm thử bằng user analyst | 15 phút | 6.3, 7.3 |
| 7 | Thu hồi quyền, thử lại, khôi phục | 5 phút | 7.5 |
| 8 | Job và danh tính Run as | 15 phút | 4.3, 4.4 |
| 9 | Ghi nhận kết quả, dọn dẹp | 5 phút | Tổng hợp |

### 1.2. Vai trò và môi trường

Lab cần **ba danh tính khác nhau**. Không dùng tài khoản quản trị để đại diện kết quả kiểm thử của hai vai trò.

| Danh tính | Thuộc nhóm | Làm gì trong lab |
| --- | --- | --- |
| Quản trị viên lab | Có quyền tạo catalog và quản lý quyền | Tạo dữ liệu, cấp và thu hồi quyền, cấu hình job |
| User kỹ sư | `lab_engineers` | Kiểm thử phần 5, là danh tính Run as ở phần 8 |
| User analyst | Chỉ `lab_analysts` | Kiểm thử phần 6 và 7 |

Hai user thử nghiệm không phải admin, không sở hữu các bảng mẫu và không nhận quyền rộng hơn thiết kế từ nhóm khác. Workspace cần:

- Unity Catalog được bật và truy cập được metastore.
- Một SQL warehouse hoặc compute tương thích Unity Catalog; cả ba danh tính đều được dùng compute này.
- Managed storage mặc định cho catalog mới, hoặc một managed location hợp lệ. Xem [điều kiện tạo catalog][db-create-catalog].
- Hai **account group** `lab_engineers`, `lab_analysts`. Workspace-local group không dùng để cấp quyền trên dữ liệu Unity Catalog. Xem [Manage groups][db-manage-groups].

> **Databricks Free Edition:** theo [trang giới hạn của Free Edition][db-free-limits] (đối chiếu 11/11/2026), mỗi tài khoản có một workspace và một metastore, chỉ có serverless compute, một SQL warehouse cỡ 2X-Small, không có account console và không hỗ trợ SCIM. Trang này không nói rõ có mời thêm user, tạo account group hay chạy `CREATE CATALOG` được hay không. Vì vậy cần thử trước ba việc đó trên Free Edition; nếu không được, dùng workspace của tổ chức hoặc nhà trường. Nếu chỉ có một tài khoản quản trị, vẫn làm được phần 3, 4 và 8, nhưng chưa xác nhận được hành vi phân quyền của hai vai trò.

### 1.3. Sản phẩm cần nộp

Mỗi nhóm nộp một báo cáo ngắn gồm các bằng chứng **E1–E8** (ảnh chụp kết quả hoặc thông báo lỗi, kèm danh tính đang chạy) và câu trả lời cho các câu hỏi **Q1–Q6** ở cuối từng phần.

| Mã | Bằng chứng | Phần |
| --- | --- | --- |
| E1 | Ba schema `bronze`, `silver`, `gold` trong Catalog Explorer | 3 |
| E2 | Bảng `gold.daily_sales` với hai dòng, tổng doanh thu 400.00 | 3 |
| E3 | Kết quả `SHOW GRANTS` trên catalog, schema gold và bảng gold | 4 |
| E4 | User kỹ sư: `current_user()`, số dòng 5 và 3, bảng thử tạo được | 5 |
| E5 | User kỹ sư bị từ chối khi đọc gold | 5 |
| E6 | User analyst đọc được gold và bị từ chối ở bốn thao tác còn lại | 6 |
| E7 | User analyst bị từ chối sau `REVOKE` | 7 |
| E8 | Run của job: `run_identity`, `clean_rows`, `total_amount` | 8 |

## 2. Kiểm tra môi trường và thiết kế quyền

### 2.1. Kiểm tra danh tính và compute

Mỗi người mở SQL editor, chọn compute của lab và chạy:

```sql
SELECT current_user() AS executing_user;
```

Ghi lại email của ba danh tính. Nếu không chọn được compute hoặc câu lệnh báo lỗi về compute, xử lý trước khi sang phần 3: thiếu quyền dùng compute là vấn đề khác với thiếu quyền đọc bảng.

### 2.2. Thiết kế cấu trúc và quyền trước khi chạy

Các bảng của lab:

| Bảng | Nội dung |
| --- | --- |
| `lab_governance.bronze.orders_raw` | Năm đơn hàng ban đầu |
| `lab_governance.silver.orders_clean` | Đơn đã thanh toán và có số tiền dương |
| `lab_governance.gold.daily_sales` | Số đơn hợp lệ và doanh thu theo ngày |

Ma trận quyền:

| Thao tác | Kỹ sư | Analyst |
| --- | --- | --- |
| Đọc bảng bronze mẫu | Cho phép | Từ chối |
| Thay đổi dữ liệu bảng bronze mẫu | Cho phép | Từ chối |
| Đọc và thay đổi dữ liệu bảng silver mẫu | Cho phép | Từ chối |
| Tạo bảng trong silver | Cho phép | Từ chối |
| Đọc bảng gold mẫu | Từ chối | Cho phép |
| Thay đổi dữ liệu bảng gold mẫu | Từ chối | Từ chối |
| Tạo bảng trong gold | Từ chối | Từ chối |

Kỹ sư không có quyền trên gold là lựa chọn của lab để quan sát ranh giới quyền; một pipeline thực tế có thể cần tập quyền khác.

## 3. Tạo catalog, schema và dữ liệu

### 3.1. Tạo catalog và schema

**Danh tính thực hiện: quản trị viên lab.**

```sql
CREATE CATALOG lab_governance;

CREATE SCHEMA lab_governance.bronze;
CREATE SCHEMA lab_governance.silver;
CREATE SCHEMA lab_governance.gold;
```

Dùng một catalog lab riêng. Nếu tên `lab_governance` đã tồn tại, chọn tên khác rồi thay nhất quán trong mọi câu lệnh. Các lệnh cố ý không dùng `IF NOT EXISTS` để tránh tiếp tục trên tài sản và grant của lần thực hành cũ. Nếu `CREATE CATALOG` báo thiếu managed location, quản trị viên cần tạo catalog với một managed location hợp lệ.

Mở Catalog Explorer, tìm `lab_governance` và kiểm tra ba schema vừa tạo. Catalog có thể chứa thêm schema do hệ thống tạo sẵn.

**E1:** chụp ba schema trong Catalog Explorer.

### 3.2. Tạo bảng đơn hàng gốc

```sql
CREATE TABLE lab_governance.bronze.orders_raw (
    order_id STRING,
    customer_id STRING,
    order_date DATE,
    status STRING,
    amount DECIMAL(12,2)
) USING DELTA;

INSERT INTO lab_governance.bronze.orders_raw VALUES
    ('o1001', 'c01', DATE '2026-10-26', 'paid', 120.00),
    ('o1002', 'c02', DATE '2026-10-26', 'paid', 80.00),
    ('o1003', 'c01', DATE '2026-10-26', 'cancelled', 50.00),
    ('o1004', 'c03', DATE '2026-10-27', 'paid', -20.00),
    ('o1005', 'c02', DATE '2026-10-27', 'paid', 200.00);

SELECT * FROM lab_governance.bronze.orders_raw ORDER BY order_id;
```

Kết quả kỳ vọng:

| order_id | customer_id | order_date | status | amount |
| --- | --- | --- | --- | --- |
| o1001 | c01 | 2026-10-26 | paid | 120.00 |
| o1002 | c02 | 2026-10-26 | paid | 80.00 |
| o1003 | c01 | 2026-10-26 | cancelled | 50.00 |
| o1004 | c03 | 2026-10-27 | paid | -20.00 |
| o1005 | c02 | 2026-10-27 | paid | 200.00 |

Đơn `o1003` đã hủy và `o1004` có số tiền âm; quy tắc của lab là không tính hai đơn này vào doanh thu.

### 3.3. Tạo bảng sạch và bảng tổng hợp

```sql
CREATE TABLE lab_governance.silver.orders_clean
USING DELTA AS
SELECT order_id, customer_id, order_date, amount
FROM lab_governance.bronze.orders_raw
WHERE status = 'paid'
  AND amount > 0;

CREATE TABLE lab_governance.gold.daily_sales
USING DELTA AS
SELECT order_date, COUNT(*) AS order_count, SUM(amount) AS revenue
FROM lab_governance.silver.orders_clean
GROUP BY order_date;

SELECT * FROM lab_governance.gold.daily_sales ORDER BY order_date;
```

`CREATE TABLE ... AS SELECT` (CTAS) tạo bảng từ kết quả truy vấn. Silver giữ ba đơn hợp lệ; gold gom các đơn theo ngày. Kết quả kỳ vọng:

| order_date | order_count | revenue |
| --- | --- | --- |
| 2026-10-26 | 2 | 200.00 |
| 2026-10-27 | 1 | 200.00 |

Tổng doanh thu kỳ vọng là **400.00**. Hai bảng này lưu kết quả tại thời điểm tạo; chúng không tự cập nhật khi bronze thay đổi.

**E2:** chụp kết quả `daily_sales`.

**Q1.** Nếu quản trị viên thêm một đơn `paid` mới vào bronze sau bước này, `gold.daily_sales` có thay đổi không? Cần làm gì để gold phản ánh đơn mới?

## 4. Cấp quyền theo nhóm

### 4.1. Nhóm kỹ sư

**Danh tính thực hiện: quản trị viên lab.**

```sql
GRANT USE CATALOG ON CATALOG lab_governance TO `lab_engineers`;
GRANT USE SCHEMA ON SCHEMA lab_governance.bronze TO `lab_engineers`;
GRANT USE SCHEMA ON SCHEMA lab_governance.silver TO `lab_engineers`;
GRANT CREATE TABLE ON SCHEMA lab_governance.silver TO `lab_engineers`;

GRANT SELECT, MODIFY ON TABLE lab_governance.bronze.orders_raw TO `lab_engineers`;
GRANT SELECT, MODIFY ON TABLE lab_governance.silver.orders_clean TO `lab_engineers`;
```

### 4.2. Nhóm analyst và kiểm tra cấu hình

```sql
GRANT USE CATALOG ON CATALOG lab_governance TO `lab_analysts`;
GRANT USE SCHEMA ON SCHEMA lab_governance.gold TO `lab_analysts`;
GRANT SELECT ON TABLE lab_governance.gold.daily_sales TO `lab_analysts`;

SHOW GRANTS ON CATALOG lab_governance;
SHOW GRANTS ON SCHEMA lab_governance.gold;
SHOW GRANTS ON TABLE lab_governance.gold.daily_sales;
```

Đối chiếu các grant với ma trận ở 2.2. Xem grant mới là kiểm tra **cấu hình**; phần 5 và 6 kiểm tra **hành vi** bằng từng user.

**E3:** chụp ba kết quả `SHOW GRANTS`.

**Q2.** Nếu bỏ câu `GRANT USE SCHEMA ON SCHEMA lab_governance.gold` của analyst, analyst còn đọc được `daily_sales` không? Vì sao?

## 5. Kiểm thử bằng user kỹ sư

**Danh tính thực hiện: user thuộc `lab_engineers`, không phải admin.**

```sql
SELECT current_user() AS executing_user;

SELECT COUNT(*) AS raw_rows FROM lab_governance.bronze.orders_raw;
SELECT COUNT(*) AS clean_rows FROM lab_governance.silver.orders_clean;
```

Kỳ vọng lần lượt là **5** và **3**. Kiểm tra quyền sửa bằng một câu UPDATE giữ nguyên giá trị:

```sql
UPDATE lab_governance.silver.orders_clean
SET amount = amount
WHERE order_id = 'o1001';
```

Kiểm tra quyền tạo bảng trong silver:

```sql
CREATE TABLE lab_governance.silver.engineer_probe
USING DELTA AS
SELECT * FROM lab_governance.silver.orders_clean LIMIT 1;

SELECT * FROM lab_governance.silver.engineer_probe;
DROP TABLE lab_governance.silver.engineer_probe;
```

Kỳ vọng tạo, đọc và xóa được bảng thử. Cuối cùng, chạy riêng câu sau để kiểm tra ranh giới với gold:

```sql
SELECT * FROM lab_governance.gold.daily_sales;
```

Theo ma trận, câu lệnh này phải bị từ chối. Nếu thành công, kiểm tra các quyền bổ sung mà user nhận được trước khi đi tiếp.

**E4, E5:** chụp `current_user()`, hai số đếm, bảng thử, và thông báo lỗi khi đọc gold.

**Q3.** User kỹ sư xóa được `engineer_probe`. Điều đó có chứng minh user xóa được `orders_clean` không? Vì sao?

## 6. Kiểm thử bằng user analyst

**Danh tính thực hiện: user thuộc `lab_analysts`, không phải admin, không thuộc `lab_engineers`.**

```sql
SELECT current_user() AS executing_user;
SELECT * FROM lab_governance.gold.daily_sales ORDER BY order_date;
```

Kỳ vọng nhận hai dòng doanh thu như ở 3.3. Sau đó chạy **từng câu riêng** và ghi nhận kết quả của mỗi câu:

```sql
SELECT * FROM lab_governance.bronze.orders_raw;
```

```sql
SELECT * FROM lab_governance.silver.orders_clean;
```

```sql
DELETE FROM lab_governance.gold.daily_sales
WHERE order_date = DATE '1900-01-01';
```

```sql
CREATE TABLE lab_governance.gold.analyst_probe (id INT);
```

Kỳ vọng cả bốn câu bị từ chối vì thiếu quyền; nội dung thông báo có thể khác nhau tùy bước kiểm tra quyền. Nếu câu CREATE thành công ngoài dự kiến, ghi lại hiện tượng và nhờ quản trị viên xóa bảng thử sau khi tìm ra nguyên nhân.

**E6:** chụp kết quả đọc gold và bốn thông báo từ chối.

**Q4.** Vì sao câu DELETE dùng ngày `1900-01-01`, một ngày không có trong dữ liệu mẫu?

## 7. Thu hồi quyền

**Quản trị viên lab** thu hồi quyền đọc của nhóm analyst:

```sql
REVOKE SELECT ON TABLE lab_governance.gold.daily_sales FROM `lab_analysts`;
```

**User analyst** chạy lại truy vấn:

```sql
SELECT * FROM lab_governance.gold.daily_sales;
```

Kỳ vọng truy vấn bị từ chối nếu không còn nguồn cấp quyền khác. Ghi lại kết quả, sau đó **quản trị viên** khôi phục quyền:

```sql
GRANT SELECT ON TABLE lab_governance.gold.daily_sales TO `lab_analysts`;
```

Không chạy REVOKE và GRANT liên tiếp rồi mới thử bằng analyst: khi đó bạn đã bỏ qua thời điểm quyền bị thu hồi.

**E7:** chụp thông báo từ chối sau REVOKE.

**Q5.** Nếu analyst vẫn đọc được bảng sau REVOKE, bạn kiểm tra những nguồn quyền nào, theo thứ tự nào?

## 8. Job và danh tính Run as

Quản trị viên tạo một notebook ngôn ngữ SQL, ví dụ `/Shared/governance-lab/check_silver`, với nội dung:

```sql
SELECT current_user() AS run_identity;

SELECT COUNT(*) AS clean_rows, SUM(amount) AS total_amount
FROM lab_governance.silver.orders_clean;
```

Tạo một job gồm một notebook task trỏ đến notebook này, chọn compute hỗ trợ notebook task và Unity Catalog (serverless nếu workspace có). Trong phần **Run as**, chọn user kỹ sư; người cấu hình phải có quyền đặt danh tính Run as tương ứng, và user kỹ sư cần quyền đọc notebook. Xem [quyền và danh tính của Jobs][db-job-permissions].

Chạy job một lần, mở run và trả lời:

1. Task có hoàn thành không?
2. `run_identity` hiển thị danh tính nào: người bấm chạy hay danh tính Run as?
3. `clean_rows` có bằng 3 và `total_amount` có bằng 400.00 không?

Task này chỉ đọc silver; nó chưa làm sạch bronze hay làm mới gold.

**E8:** chụp trang run có kết quả của hai câu SELECT.

**Q6.** Quản trị viên bấm chạy job này. Nếu Run as là user analyst thay vì kỹ sư, task sẽ ra sao? Kết quả đó nói gì về quyền của người bấm chạy?

## 9. Ghi nhận kết quả và dọn dẹp

### 9.1. Bảng ghi nhận

| Danh tính | Phép thử | Kỳ vọng | Kết quả thực tế |
| --- | --- | --- | --- |
| Kỹ sư | Đếm dòng bronze và silver | 5 và 3 | Điền sau khi chạy |
| Kỹ sư | UPDATE bảng silver | Thành công | Điền sau khi chạy |
| Kỹ sư | Tạo bảng thử trong silver | Thành công | Điền sau khi chạy |
| Kỹ sư | Đọc bảng gold | Bị từ chối | Điền sau khi chạy |
| Analyst | Đọc bảng gold | Hai dòng tổng hợp | Điền sau khi chạy |
| Analyst | Đọc bronze, đọc silver | Đều bị từ chối | Điền sau khi chạy |
| Analyst | DELETE dữ liệu gold | Bị từ chối | Điền sau khi chạy |
| Analyst | Tạo bảng trong gold | Bị từ chối | Điền sau khi chạy |
| Analyst sau REVOKE | Đọc bảng gold | Bị từ chối | Điền sau khi chạy |
| Job chạy bằng kỹ sư | Kiểm tra silver | 3 dòng, tổng 400.00 | Điền sau khi chạy |

### 9.2. Dọn dẹp

Khi đã nộp bằng chứng, quản trị viên xóa job, notebook và catalog lab cùng mọi đối tượng bên trong:

```sql
DROP CATALOG lab_governance CASCADE;
```

Lệnh này xóa vĩnh viễn ba schema và các bảng managed trong catalog. Chỉ chạy trên catalog dành riêng cho lab.

## 10. Lỗi thường gặp và cách suy luận

| Hiện tượng | Cách suy luận |
| --- | --- |
| Có SELECT nhưng vẫn không đọc được | Kiểm tra tên đầy đủ, `USE CATALOG`, `USE SCHEMA`, workspace binding của catalog và quyền dùng compute |
| Analyst đọc được dữ liệu ngoài dự kiến | Kiểm tra `current_user()`; xem user có phải owner, admin, thành viên nhóm kỹ sư hay nhóm khác; đối chiếu grant ở catalog, schema, table |
| Đã REVOKE nhưng vẫn đọc được | Xác định grant vừa thu hồi; user có thể còn SELECT từ schema, catalog hoặc group khác; chắc chắn đang chạy bằng user analyst |
| Notebook chạy được nhưng job thất bại | So sánh danh tính khi chạy tương tác với Run as; kiểm tra quyền notebook, compute và dữ liệu của danh tính thực thi; mở đúng run, đúng task |
| Bronze thay đổi nhưng gold không đổi | Silver và gold tạo bằng CTAS; cần chạy lại logic biến đổi mà không nhân đôi bản ghi |
| `CREATE CATALOG` báo thiếu vị trí lưu trữ | Metastore chưa có managed storage mặc định; quản trị viên cần chỉ định managed location hợp lệ |

## 11. Bài tập mở rộng

**Bài tập A — Thêm khu vực thử nghiệm.** Tạo schema `sandbox` để kỹ sư tự tạo bảng. Viết trước những quyền kỹ sư cần và dữ liệu họ được phép đọc làm đầu vào.

**Bài tập B — Thêm vai trò chỉ đọc.** Thiết kế nhóm chỉ được đọc một bảng cụ thể trong silver. So sánh SELECT trên bảng với SELECT trên toàn schema.

**Bài tập C — Tách danh tính tự động hóa.** Đề xuất quyền cho một service principal chạy job ở phần 8. Liệt kê quyền trên notebook, compute và bảng.

**Bài tập D — Tìm nguồn của quyền.** Tạo tình huống user nhận SELECT qua hai group, thu hồi từ một group rồi giải thích kết quả truy vấn.

**Bài tập E — Khám phá lineage.** Nếu workspace hỗ trợ và bạn có quyền, mở lineage của `daily_sales` và đối chiếu với các câu CTAS ở phần 3.

## Tài liệu tham khảo

- [Compute][db-compute]
- [Manage identities, permissions, and privileges for Lakeflow Jobs][db-job-permissions]
- [Access control in Unity Catalog][db-access]
- [Unity Catalog privileges reference][db-privileges]
- [Manage privileges in Unity Catalog][db-manage-privileges]
- [Manage groups][db-manage-groups]
- [Create catalogs][db-create-catalog]
- [Free Edition limitations][db-free-limits]
- [Lineage in Unity Catalog][db-lineage]

[db-compute]: https://docs.databricks.com/aws/en/compute/
[db-job-permissions]: https://docs.databricks.com/aws/en/jobs/privileges
[db-access]: https://docs.databricks.com/aws/en/data-governance/unity-catalog/access-control/
[db-privileges]: https://docs.databricks.com/aws/en/data-governance/unity-catalog/access-control/privileges-reference
[db-manage-privileges]: https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges/
[db-manage-groups]: https://docs.databricks.com/aws/en/admin/users-groups/manage-groups
[db-create-catalog]: https://docs.databricks.com/aws/en/catalogs/create-catalog
[db-free-limits]: https://docs.databricks.com/aws/en/getting-started/free-edition-limitations
[db-lineage]: https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-lineage
