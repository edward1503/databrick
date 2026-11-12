-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Lab Governance — 04. Quản trị viên: thu hồi và khôi phục quyền
-- MAGIC
-- MAGIC **Danh tính chạy notebook:** quản trị viên lab. Làm phần 7 của hướng dẫn lab.
-- MAGIC
-- MAGIC Thứ tự bắt buộc:
-- MAGIC 1. Quản trị viên chạy ô REVOKE.
-- MAGIC 2. User analyst chạy ô cuối của notebook 03 và ghi lại kết quả.
-- MAGIC 3. Quản trị viên mới chạy ô GRANT để khôi phục.

-- COMMAND ----------

REVOKE SELECT ON TABLE lab_governance.gold.daily_sales FROM `lab_analysts`;

-- COMMAND ----------

SHOW GRANTS ON TABLE lab_governance.gold.daily_sales;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **Dừng ở đây** cho đến khi analyst đã chạy thử. Sau đó khôi phục quyền:

-- COMMAND ----------

GRANT SELECT ON TABLE lab_governance.gold.daily_sales TO `lab_analysts`;
