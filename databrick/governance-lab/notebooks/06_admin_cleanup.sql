-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Lab Governance — 06. Quản trị viên: dọn dẹp
-- MAGIC
-- MAGIC Chỉ chạy sau khi mọi nhóm đã nộp bằng chứng. Xóa job của phần 8 trong **Jobs & Pipelines** trước.
-- MAGIC
-- MAGIC Lệnh dưới **xóa vĩnh viễn** catalog `lab_governance`, ba schema và mọi bảng managed bên trong.
-- MAGIC Chỉ chạy trên catalog dành riêng cho lab.

-- COMMAND ----------

DROP CATALOG lab_governance CASCADE;
