-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Lab Governance — 03. User analyst: kiểm thử quyền
-- MAGIC
-- MAGIC **Danh tính chạy notebook:** user chỉ thuộc `lab_analysts`, không phải admin.
-- MAGIC Làm phần 6 và 7 của hướng dẫn lab.
-- MAGIC
-- MAGIC **Bằng chứng E6:** kết quả đọc gold và bốn thông báo từ chối.
-- MAGIC **Bằng chứng E7:** thông báo từ chối ở ô cuối, sau khi quản trị viên chạy REVOKE.

-- COMMAND ----------

SELECT current_user() AS executing_user;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Kỳ vọng 2 dòng doanh thu, tổng 400.00.

-- COMMAND ----------

SELECT * FROM lab_governance.gold.daily_sales ORDER BY order_date;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Bốn thao tác ngoài phạm vi: mỗi ô phải bị từ chối
-- MAGIC
-- MAGIC Chạy **từng ô riêng** và ghi nguyên văn thông báo. Câu DELETE dùng ngày không có trong
-- MAGIC dữ liệu mẫu để không xóa gì nếu quyền đang rộng hơn thiết kế.

-- COMMAND ----------

SELECT * FROM lab_governance.bronze.orders_raw;

-- COMMAND ----------

SELECT * FROM lab_governance.silver.orders_clean;

-- COMMAND ----------

DELETE FROM lab_governance.gold.daily_sales
WHERE order_date = DATE '1900-01-01';

-- COMMAND ----------

CREATE TABLE lab_governance.gold.analyst_probe (id INT);

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Sau khi quản trị viên thu hồi quyền
-- MAGIC
-- MAGIC Chỉ chạy ô dưới **sau khi** quản trị viên đã chạy ô REVOKE trong notebook 04 và
-- MAGIC **trước khi** quản trị viên khôi phục quyền. Kỳ vọng bị từ chối.

-- COMMAND ----------

SELECT * FROM lab_governance.gold.daily_sales;
