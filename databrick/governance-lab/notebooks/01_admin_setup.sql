-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Lab Governance — 01. Quản trị viên: tạo dữ liệu và cấp quyền
-- MAGIC
-- MAGIC **Danh tính chạy notebook:** quản trị viên lab (có quyền tạo catalog và quản lý quyền).
-- MAGIC
-- MAGIC Notebook này làm phần 2.1, 3 và 4 của hướng dẫn lab. Chạy **từng ô theo thứ tự**.
-- MAGIC Trước khi chạy, bảo đảm đã có hai account group `lab_engineers`, `lab_analysts`
-- MAGIC và mỗi group có một user thử nghiệm không phải admin.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 2.1. Kiểm tra danh tính đang chạy

-- COMMAND ----------

SELECT current_user() AS executing_user;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 3.1. Tạo catalog và schema
-- MAGIC
-- MAGIC Cố ý không dùng `IF NOT EXISTS`: nếu `lab_governance` đã tồn tại, đổi tên catalog
-- MAGIC nhất quán trong mọi notebook thay vì dùng lại tài sản của lần trước.
-- MAGIC **Bằng chứng E1:** mở Catalog Explorer, chụp ba schema `bronze`, `silver`, `gold`.

-- COMMAND ----------

CREATE CATALOG lab_governance;

-- COMMAND ----------

CREATE SCHEMA lab_governance.bronze;
CREATE SCHEMA lab_governance.silver;
CREATE SCHEMA lab_governance.gold;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 3.2. Bảng đơn hàng gốc (bronze)
-- MAGIC
-- MAGIC Kỳ vọng 5 dòng. `o1003` đã hủy, `o1004` có số tiền âm: hai đơn này không được tính doanh thu.

-- COMMAND ----------

CREATE TABLE lab_governance.bronze.orders_raw (
    order_id STRING,
    customer_id STRING,
    order_date DATE,
    status STRING,
    amount DECIMAL(12,2)
) USING DELTA;

-- COMMAND ----------

INSERT INTO lab_governance.bronze.orders_raw VALUES
    ('o1001', 'c01', DATE '2026-10-26', 'paid', 120.00),
    ('o1002', 'c02', DATE '2026-10-26', 'paid', 80.00),
    ('o1003', 'c01', DATE '2026-10-26', 'cancelled', 50.00),
    ('o1004', 'c03', DATE '2026-10-27', 'paid', -20.00),
    ('o1005', 'c02', DATE '2026-10-27', 'paid', 200.00);

-- COMMAND ----------

SELECT * FROM lab_governance.bronze.orders_raw ORDER BY order_id;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 3.3. Bảng sạch (silver) và bảng tổng hợp (gold)
-- MAGIC
-- MAGIC Kỳ vọng gold có 2 dòng: 2026-10-26 (2 đơn, 200.00) và 2026-10-27 (1 đơn, 200.00); tổng 400.00.
-- MAGIC **Bằng chứng E2:** chụp kết quả ô SELECT cuối.

-- COMMAND ----------

CREATE TABLE lab_governance.silver.orders_clean
USING DELTA AS
SELECT order_id, customer_id, order_date, amount
FROM lab_governance.bronze.orders_raw
WHERE status = 'paid'
  AND amount > 0;

-- COMMAND ----------

CREATE TABLE lab_governance.gold.daily_sales
USING DELTA AS
SELECT order_date, COUNT(*) AS order_count, SUM(amount) AS revenue
FROM lab_governance.silver.orders_clean
GROUP BY order_date;

-- COMMAND ----------

SELECT * FROM lab_governance.gold.daily_sales ORDER BY order_date;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 4.1. Cấp quyền cho nhóm kỹ sư

-- COMMAND ----------

GRANT USE CATALOG ON CATALOG lab_governance TO `lab_engineers`;
GRANT USE SCHEMA ON SCHEMA lab_governance.bronze TO `lab_engineers`;
GRANT USE SCHEMA ON SCHEMA lab_governance.silver TO `lab_engineers`;
GRANT CREATE TABLE ON SCHEMA lab_governance.silver TO `lab_engineers`;
GRANT SELECT, MODIFY ON TABLE lab_governance.bronze.orders_raw TO `lab_engineers`;
GRANT SELECT, MODIFY ON TABLE lab_governance.silver.orders_clean TO `lab_engineers`;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 4.2. Cấp quyền cho nhóm analyst và xem grant
-- MAGIC
-- MAGIC **Bằng chứng E3:** chụp ba kết quả `SHOW GRANTS`, hoặc tab **Permissions** của bảng
-- MAGIC `daily_sales` trong Catalog Explorer.

-- COMMAND ----------

GRANT USE CATALOG ON CATALOG lab_governance TO `lab_analysts`;
GRANT USE SCHEMA ON SCHEMA lab_governance.gold TO `lab_analysts`;
GRANT SELECT ON TABLE lab_governance.gold.daily_sales TO `lab_analysts`;

-- COMMAND ----------

SHOW GRANTS ON CATALOG lab_governance;

-- COMMAND ----------

SHOW GRANTS ON SCHEMA lab_governance.gold;

-- COMMAND ----------

SHOW GRANTS ON TABLE lab_governance.gold.daily_sales;
