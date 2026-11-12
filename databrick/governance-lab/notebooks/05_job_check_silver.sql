-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Lab Governance — 05. Notebook cho job (Run as)
-- MAGIC
-- MAGIC Notebook này được chạy **bởi một job**, không chạy tay. Làm phần 8 của hướng dẫn lab:
-- MAGIC tạo job có một notebook task trỏ tới notebook này, đặt **Run as** là user kỹ sư,
-- MAGIC rồi để quản trị viên bấm chạy.
-- MAGIC
-- MAGIC Kỳ vọng: `run_identity` là danh tính Run as (user kỹ sư), `clean_rows = 3`, `total_amount = 400.00`.
-- MAGIC **Bằng chứng E8:** trang run hiển thị kết quả hai ô dưới.

-- COMMAND ----------

SELECT current_user() AS run_identity;

-- COMMAND ----------

SELECT COUNT(*) AS clean_rows, SUM(amount) AS total_amount
FROM lab_governance.silver.orders_clean;
