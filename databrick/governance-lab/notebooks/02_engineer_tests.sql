-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Lab Governance — 02. User kỹ sư: kiểm thử quyền
-- MAGIC
-- MAGIC **Danh tính chạy notebook:** user thuộc `lab_engineers`, không phải admin.
-- MAGIC Làm phần 5 của hướng dẫn lab. Chạy từng ô; ghi lại kết quả của mỗi ô.
-- MAGIC
-- MAGIC **Bằng chứng E4:** `current_user()`, hai số đếm, bảng thử tạo được.
-- MAGIC **Bằng chứng E5:** thông báo lỗi ở ô cuối (đọc gold).

-- COMMAND ----------

SELECT current_user() AS executing_user;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Kỳ vọng `raw_rows = 5`, `clean_rows = 3`.

-- COMMAND ----------

SELECT
    (SELECT COUNT(*) FROM lab_governance.bronze.orders_raw) AS raw_rows,
    (SELECT COUNT(*) FROM lab_governance.silver.orders_clean) AS clean_rows;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Kiểm tra quyền sửa bằng một câu UPDATE giữ nguyên giá trị (không làm đổi dữ liệu mẫu).

-- COMMAND ----------

UPDATE lab_governance.silver.orders_clean
SET amount = amount
WHERE order_id = 'o1001';

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Kiểm tra quyền tạo bảng trong silver. Kỳ vọng tạo, đọc và xóa được bảng thử.

-- COMMAND ----------

CREATE TABLE lab_governance.silver.engineer_probe
USING DELTA AS
SELECT * FROM lab_governance.silver.orders_clean LIMIT 1;

-- COMMAND ----------

SELECT * FROM lab_governance.silver.engineer_probe;

-- COMMAND ----------

DROP TABLE lab_governance.silver.engineer_probe;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Ranh giới với gold
-- MAGIC
-- MAGIC Theo ma trận quyền, ô dưới **phải bị từ chối**. Nếu chạy thành công, dừng lại và
-- MAGIC tìm nguồn quyền bổ sung (owner, admin, group khác, grant ở catalog hay schema).

-- COMMAND ----------

SELECT * FROM lab_governance.gold.daily_sales;
