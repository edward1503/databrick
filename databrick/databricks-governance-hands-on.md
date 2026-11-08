# Hands-on: Databricks & Governance Basics

*Tổ chức catalog, schema, table và kiểm tra quyền truy cập mẫu*

**Bài đọc nền tảng:** [Databricks & Governance Basics](databricks-governance-basics.md).

**Mục tiêu:** tạo dữ liệu đơn hàng, xây dựng ma trận quyền cho kỹ sư và analyst, kiểm thử bằng từng danh tính và quan sát Run as của một job.

**Kiến thức cần có:** SQL cơ bản và các khái niệm workspace, compute, jobs, namespace, principal, grant trong bài đọc nền tảng.

> **Phạm vi và trạng thái:** hướng dẫn sử dụng Unity Catalog và managed Delta tables, giả định môi trường có các quyền quản trị và danh tính cần thiết. Các kết quả được ghi là kỳ vọng; lab chưa được chạy trên một workspace cụ thể. Phần thao tác trên Databricks Free Edition và ảnh chụp thực tế sẽ được bổ sung sau khi thực hành.

## 1. Lab: tổ chức catalog, schema, table và quyền truy cập

### 1.1. Mục tiêu và điều kiện chuẩn bị

Lab tạo dữ liệu mẫu và phân quyền cho hai vai trò. Sau khi hoàn thành, kỹ sư có thể làm việc với bronze/silver, còn analyst chỉ đọc bảng tổng hợp được chỉ định trong gold.

Chuẩn bị các điều kiện sau:

- Workspace đã bật Unity Catalog và truy cập được metastore phù hợp.
- SQL warehouse hoặc compute tương thích Unity Catalog để chạy SQL.
- Mỗi người thử nghiệm có quyền đăng nhập workspace và sử dụng compute đã chọn.
- Một quản trị viên lab có quyền tạo catalog và quản lý quyền trên các đối tượng mẫu.
- Managed storage đã được cấu hình phù hợp.
- Hai account group `lab_engineers`, `lab_analysts` và hai user thử nghiệm khác nhau.

User kỹ sư thuộc `lab_engineers`. User analyst chỉ thuộc `lab_analysts` trong hai nhóm của lab. Hai user không phải admin, không sở hữu các bảng mẫu và không nhận quyền rộng hơn thiết kế từ nhóm khác.

Quản trị viên có thể tạo hoặc quản lý account group theo hướng dẫn [Manage groups][db-manage-groups]. Việc tạo nhóm và gán thành viên là bước quản trị danh tính, tách khỏi các câu SQL cấp quyền bảng bên dưới.

> Lệnh `CREATE CATALOG lab_governance` giả định metastore có managed storage mặc định. Nếu chưa có, quản trị viên cần tạo catalog với một managed location hợp lệ và quyền tương ứng. Xem [điều kiện tạo catalog][db-create-catalog].
>
> Dùng một catalog lab riêng. Nếu tên `lab_governance` đã tồn tại, chọn tên khác rồi thay nhất quán trong các câu lệnh. Các lệnh tạo bên dưới cố ý không dùng `IF NOT EXISTS` để tránh tiếp tục trên tài sản và grant của lần thực hành cũ.

### 1.2. Thiết kế cấu trúc và quyền trước khi chạy

Các bảng của lab:

| Bảng | Nội dung |
| --- | --- |
| `lab_governance.bronze.orders_raw` | Năm đơn hàng ban đầu. |
| `lab_governance.silver.orders_clean` | Đơn đã thanh toán và có số tiền dương. |
| `lab_governance.gold.daily_sales` | Số đơn hợp lệ và doanh thu theo ngày. |

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

Quản trị viên là người chuẩn bị dữ liệu và quyền, không dùng tài khoản này để đại diện kết quả kiểm thử của hai vai trò.

### 1.3. Bước 1: tạo catalog và schema

**Danh tính thực hiện: quản trị viên lab.**

Mở SQL editor hoặc notebook có ngôn ngữ SQL, chọn compute phù hợp rồi chạy:

```sql
CREATE CATALOG lab_governance;

CREATE SCHEMA lab_governance.bronze;
CREATE SCHEMA lab_governance.silver;
CREATE SCHEMA lab_governance.gold;
```

Mở Catalog Explorer, tìm `lab_governance` và kiểm tra ba schema vừa tạo. Catalog cũng có thể chứa các schema được hệ thống tạo sẵn; ba schema trong bài là những schema do chúng ta chủ động tạo.

### 1.4. Bước 2: tạo bảng đơn hàng gốc

**Danh tính thực hiện: quản trị viên lab.**

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

SELECT *
FROM lab_governance.bronze.orders_raw
ORDER BY order_id;
```

Kết quả kỳ vọng:

| order_id | customer_id | order_date | status | amount |
| --- | --- | --- | --- | ---: |
| o1001 | c01 | 2026-10-26 | paid | 120.00 |
| o1002 | c02 | 2026-10-26 | paid | 80.00 |
| o1003 | c01 | 2026-10-26 | cancelled | 50.00 |
| o1004 | c03 | 2026-10-27 | paid | -20.00 |
| o1005 | c02 | 2026-10-27 | paid | 200.00 |

Hai dòng được đưa vào để minh họa quy tắc nghiệp vụ: `o1003` đã hủy, còn `o1004` có số tiền âm. Quy tắc của lab là không tính hai đơn này vào doanh thu.

### 1.5. Bước 3: tạo bảng sạch và bảng tổng hợp

**Danh tính thực hiện: quản trị viên lab.**

```sql
CREATE TABLE lab_governance.silver.orders_clean
USING DELTA AS
SELECT
    order_id,
    customer_id,
    order_date,
    amount
FROM lab_governance.bronze.orders_raw
WHERE status = 'paid'
  AND amount > 0;

CREATE TABLE lab_governance.gold.daily_sales
USING DELTA AS
SELECT
    order_date,
    COUNT(*) AS order_count,
    SUM(amount) AS revenue
FROM lab_governance.silver.orders_clean
GROUP BY order_date;

SELECT *
FROM lab_governance.gold.daily_sales
ORDER BY order_date;
```

`CREATE TABLE ... AS SELECT`, thường gọi là **CTAS**, tạo bảng từ kết quả truy vấn. Trong ví dụ này, silver giữ ba đơn hợp lệ; gold gom các đơn theo ngày.

| order_date | order_count | revenue |
| --- | ---: | ---: |
| 2026-10-26 | 2 | 200.00 |
| 2026-10-27 | 1 | 200.00 |

Tổng doanh thu kỳ vọng là **400.00**. Những bảng này lưu kết quả tại thời điểm tạo. Nếu dữ liệu bronze thay đổi, silver và gold không tự cập nhật chỉ vì các câu CTAS trên đã được chạy một lần.

### 1.6. Bước 4: cấp quyền cho nhóm kỹ sư

**Danh tính thực hiện: quản trị viên lab.**

Đầu tiên, mở quyền sử dụng namespace và quyền tạo bảng trong silver:

```sql
GRANT USE CATALOG ON CATALOG lab_governance
TO `lab_engineers`;

GRANT USE SCHEMA ON SCHEMA lab_governance.bronze
TO `lab_engineers`;

GRANT USE SCHEMA ON SCHEMA lab_governance.silver
TO `lab_engineers`;

GRANT CREATE TABLE ON SCHEMA lab_governance.silver
TO `lab_engineers`;
```

Tiếp theo, cấp quyền đọc và thay đổi dữ liệu trên hai bảng mẫu:

```sql
GRANT SELECT, MODIFY
ON TABLE lab_governance.bronze.orders_raw
TO `lab_engineers`;

GRANT SELECT, MODIFY
ON TABLE lab_governance.silver.orders_clean
TO `lab_engineers`;
```

Nhóm kỹ sư không được cấp quyền trên gold trong thiết kế này. Đây là lựa chọn của bài thực hành để quan sát ranh giới quyền; một pipeline thực tế có thể cần một tập quyền khác theo nhiệm vụ của nó.

### 1.7. Bước 5: cấp quyền cho nhóm analyst

**Danh tính thực hiện: quản trị viên lab.**

```sql
GRANT USE CATALOG ON CATALOG lab_governance
TO `lab_analysts`;

GRANT USE SCHEMA ON SCHEMA lab_governance.gold
TO `lab_analysts`;

GRANT SELECT
ON TABLE lab_governance.gold.daily_sales
TO `lab_analysts`;
```

Sau đó xem thông tin grant:

```sql
SHOW GRANTS ON CATALOG lab_governance;
SHOW GRANTS ON SCHEMA lab_governance.gold;
SHOW GRANTS ON TABLE lab_governance.gold.daily_sales;
```

Đối chiếu các grant với ma trận đã thiết kế. Tuy nhiên, xem grant mới là kiểm tra cấu hình; các bước tiếp theo sẽ kiểm tra hành vi truy cập bằng từng user.

### 1.8. Bước 6: kiểm thử bằng user kỹ sư

**Danh tính thực hiện: user thuộc `lab_engineers`, không phải admin.**

Đăng nhập bằng user kỹ sư và kiểm tra danh tính:

```sql
SELECT current_user() AS executing_user;
```

Đọc hai bảng:

```sql
SELECT COUNT(*) AS raw_rows
FROM lab_governance.bronze.orders_raw;

SELECT COUNT(*) AS clean_rows
FROM lab_governance.silver.orders_clean;
```

Kỳ vọng lần lượt là **5** và **3**. Tiếp theo, thử một câu UPDATE giữ nguyên giá trị để kiểm tra quyền sửa mà không làm thay đổi nội dung ví dụ:

```sql
UPDATE lab_governance.silver.orders_clean
SET amount = amount
WHERE order_id = 'o1001';
```

Kiểm tra quyền tạo bảng trong silver:

```sql
CREATE TABLE lab_governance.silver.engineer_probe
USING DELTA AS
SELECT *
FROM lab_governance.silver.orders_clean
LIMIT 1;

SELECT *
FROM lab_governance.silver.engineer_probe;

DROP TABLE lab_governance.silver.engineer_probe;
```

Kỳ vọng tạo và đọc được bảng thử. User tạo bảng sở hữu bảng thử đó; việc xóa được bảng thử không chứng minh user được xóa mọi bảng trong silver.

Cuối cùng, chạy riêng câu sau để kiểm tra ranh giới với gold:

```sql
SELECT *
FROM lab_governance.gold.daily_sales;
```

Theo ma trận của lab, câu lệnh này phải bị từ chối. Nếu thành công, kiểm tra các quyền bổ sung mà user nhận được.

### 1.9. Bước 7: kiểm thử bằng user analyst

**Danh tính thực hiện: user thuộc `lab_analysts`, không phải admin và không thuộc `lab_engineers`.**

Kiểm tra danh tính rồi đọc bảng tổng hợp:

```sql
SELECT current_user() AS executing_user;

SELECT *
FROM lab_governance.gold.daily_sales
ORDER BY order_date;
```

Kỳ vọng nhận được hai dòng doanh thu như bước tạo dữ liệu.

Sau đó thực hiện **từng câu lệnh riêng** để kiểm tra các thao tác không được phép. Mỗi câu phải được ghi nhận kết quả độc lập.

**Thử đọc dữ liệu gốc:**

```sql
SELECT *
FROM lab_governance.bronze.orders_raw;
```

**Thử đọc dữ liệu silver:**

```sql
SELECT *
FROM lab_governance.silver.orders_clean;
```

**Thử thay đổi bảng doanh thu:**

```sql
DELETE FROM lab_governance.gold.daily_sales
WHERE order_date = DATE '1900-01-01';
```

**Thử tạo bảng trong gold:**

```sql
CREATE TABLE lab_governance.gold.analyst_probe (
    id INT
);
```

Kỳ vọng cả bốn thao tác đều bị từ chối vì thiếu quyền. Thông báo cụ thể có thể khác nhau tùy bước kiểm tra quyền.

Câu DELETE dùng ngày không tồn tại trong dữ liệu mẫu để tránh xóa dữ liệu nếu quyền đang rộng hơn thiết kế. Nếu câu CREATE thành công ngoài dự kiến, ghi lại hiện tượng và nhờ quản trị viên xóa bảng thử sau khi xác định nguyên nhân.

### 1.10. Bước 8: thử thu hồi quyền

**Quản trị viên lab** thu hồi quyền SELECT của nhóm analyst trên bảng gold:

```sql
REVOKE SELECT
ON TABLE lab_governance.gold.daily_sales
FROM `lab_analysts`;
```

Sau đó, **user analyst** chạy lại truy vấn trực tiếp:

```sql
SELECT *
FROM lab_governance.gold.daily_sales;
```

Kỳ vọng truy vấn bị từ chối nếu không còn nguồn cấp quyền khác. Ghi lại kết quả trước khi quản trị viên khôi phục quyền:

```sql
GRANT SELECT
ON TABLE lab_governance.gold.daily_sales
TO `lab_analysts`;
```

Không chạy REVOKE và GRANT liên tiếp rồi mới thử bằng analyst: khi đó bạn đã bỏ qua thời điểm quyền được thu hồi.

### 1.11. Bước 9: quan sát danh tính thực thi của job

Tạo một notebook có ngôn ngữ SQL chứa các câu lệnh:

```sql
SELECT current_user() AS run_identity;

SELECT
    COUNT(*) AS clean_rows,
    SUM(amount) AS total_amount
FROM lab_governance.silver.orders_clean;
```

Tạo một job gồm một notebook task trỏ đến notebook này. Chọn compute hỗ trợ notebook task và Unity Catalog, đồng thời kiểm tra cấu hình **Run as**. Trong lab, dùng user kỹ sư đã kiểm thử; người cấu hình phải có quyền đặt danh tính Run as tương ứng. Nếu có serverless compute phù hợp, có thể sử dụng lựa chọn đó theo cấu hình workspace.

Chạy job một lần rồi mở run để xem:

1. Task có hoàn thành không?
2. `run_identity` hiển thị danh tính nào?
3. `clean_rows` có bằng 3 và `total_amount` có bằng 400.00 không?

Task này chỉ đọc và kiểm tra silver. Nó chưa tự động làm sạch bronze hoặc làm mới gold. Muốn xây dựng pipeline cập nhật đầy đủ, cần bổ sung logic biến đổi và quyền cho từng bước.

### 1.12. Ghi nhận kết quả

Sử dụng bảng sau làm mẫu ghi nhận; điền kết quả sau khi thực hiện trên môi trường của bạn:

| Danh tính | Phép thử | Kỳ vọng | Kết quả thực tế |
| --- | --- | --- | --- |
| Kỹ sư | Đếm dòng bronze và silver | 5 và 3 | Chưa chạy |
| Kỹ sư | UPDATE bảng silver | Thành công | Chưa chạy |
| Kỹ sư | Tạo bảng thử trong silver | Thành công | Chưa chạy |
| Kỹ sư | Đọc bảng gold | Bị từ chối | Chưa chạy |
| Analyst | Đọc bảng gold | Hai dòng tổng hợp | Chưa chạy |
| Analyst | Đọc bronze và silver, chạy từng câu | Đều bị từ chối | Chưa chạy |
| Analyst | DELETE dữ liệu gold | Bị từ chối | Chưa chạy |
| Analyst | Tạo bảng trong gold | Bị từ chối | Chưa chạy |
| Analyst sau REVOKE | Đọc bảng gold | Bị từ chối | Chưa chạy |
| Job chạy bằng kỹ sư | Kiểm tra silver | 3 dòng, tổng tiền 400.00 | Chưa chạy |

Để kiểm tra toàn bộ ma trận, bổ sung các phép thử còn lại, chẳng hạn analyst tạo bảng trong silver hoặc kỹ sư thay đổi gold. Các câu lệnh phải được chọn sao cho không làm sai lệch dữ liệu mẫu nếu quyền rộng hơn dự kiến.

Sản phẩm cuối lab gồm cấu trúc catalog/schema/table, ma trận quyền, kết quả kiểm thử từ từng danh tính và thông tin run của job. Nếu chỉ có một tài khoản quản trị, bạn có thể thực hành tạo đối tượng và xem grant, nhưng chưa xác nhận được hành vi phân quyền của các vai trò riêng biệt.

## 2. Lỗi thường gặp và cách suy luận

### 2.1. Có SELECT nhưng vẫn không đọc được

Kiểm tra tên bảng đầy đủ, `USE CATALOG`, `USE SCHEMA` và workspace hiện tại. Nếu catalog có workspace binding, cần bảo đảm workspace đang dùng được phép truy cập catalog. Cũng cần kiểm tra user đang sử dụng đúng compute và có quyền sử dụng tài nguyên đó. Xem [kiểm soát truy cập Unity Catalog][db-access].

### 2.2. Analyst đọc được dữ liệu ngoài dự kiến

Đầu tiên, kiểm tra `current_user()`. Sau đó xem user có phải owner, admin, thành viên nhóm kỹ sư hoặc một nhóm khác đã được cấp quyền hay không. Tiếp tục đối chiếu các grant ở catalog, schema và table.

Một phép thử chạy thành công ngoài dự kiến là tín hiệu để truy vết nguồn quyền. Nó chưa đủ để kết luận câu GRANT vừa viết có phạm vi đúng.

### 2.3. Đã REVOKE nhưng vẫn đọc được

Hãy xác định grant vừa thu hồi là grant nào. Quyền trực tiếp trên bảng có thể đã được gỡ, trong khi user vẫn nhận SELECT từ schema hoặc một group khác. Cũng cần chắc chắn phép thử đang chạy bằng user analyst chứ không phải tài khoản quản trị.

### 2.4. Notebook chạy được nhưng job thất bại

So sánh danh tính khi chạy tương tác với Run as của job. Tiếp theo, kiểm tra quyền truy cập notebook, compute và dữ liệu của danh tính thực thi. Mở đúng run và đúng task để đọc lỗi thay vì suy đoán chỉ từ trạng thái chung của job.

### 2.5. Dữ liệu nguồn thay đổi nhưng bảng kết quả không đổi

Trong lab, silver và gold được tạo bằng CTAS. Một lần tạo bảng không tự thiết lập công việc cập nhật liên tục. Cần chạy logic biến đổi phù hợp để cập nhật dữ liệu và xem xét cách chạy lại mà không nhân đôi bản ghi.

## 3. Bài tập mở rộng

**Bài tập A — Thêm khu vực thử nghiệm.** Tạo schema `sandbox` để kỹ sư tự tạo bảng. Viết trước những quyền kỹ sư cần có và những dữ liệu họ được phép đọc làm đầu vào.

**Bài tập B — Thêm vai trò chỉ đọc.** Thiết kế nhóm chỉ được đọc một bảng cụ thể trong silver. So sánh lựa chọn cấp SELECT trên bảng với cấp SELECT trên toàn schema.

**Bài tập C — Tách danh tính tự động hóa.** Đề xuất quyền cho một service principal chạy job kiểm tra silver. Liệt kê quyền trên notebook, compute và bảng cần xem xét.

**Bài tập D — Tìm nguồn của quyền.** Tạo tình huống user nhận SELECT qua hai group, thu hồi từ một group rồi giải thích kết quả truy vấn. Ghi rõ nguồn quyền còn lại.

**Bài tập E — Khám phá lineage.** Nếu workspace đáp ứng điều kiện và bạn có quyền phù hợp, mở lineage của `daily_sales`, đối chiếu với các truy vấn tạo silver/gold trong lab. Ghi lại những quan hệ quan sát được.

## Tài liệu tham khảo

- [Compute][db-compute]
- [Manage identities, permissions, and privileges for Lakeflow Jobs][db-job-permissions]
- [Access control in Unity Catalog][db-access]
- [Unity Catalog privileges reference][db-privileges]
- [Manage privileges in Unity Catalog][db-manage-privileges]
- [Manage groups][db-manage-groups]
- [Create catalogs][db-create-catalog]
- [Lineage in Unity Catalog][db-lineage]

[db-compute]: https://docs.databricks.com/aws/en/compute/
[db-job-permissions]: https://docs.databricks.com/aws/en/jobs/privileges
[db-access]: https://docs.databricks.com/aws/en/data-governance/unity-catalog/access-control/
[db-privileges]: https://docs.databricks.com/aws/en/data-governance/unity-catalog/access-control/privileges-reference
[db-manage-privileges]: https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges/
[db-manage-groups]: https://docs.databricks.com/aws/en/admin/users-groups/manage-groups
[db-create-catalog]: https://docs.databricks.com/aws/en/catalogs/create-catalog
[db-lineage]: https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-lineage
