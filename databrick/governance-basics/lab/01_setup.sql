-- Run as the lab administrator in a Unity Catalog-enabled workspace.
-- Requires CREATE CATALOG and a configured metastore managed location.
-- Use a fresh, dedicated lab catalog. Do not reuse a shared catalog.
CREATE CATALOG lab_governance;

CREATE SCHEMA lab_governance.bronze;
CREATE SCHEMA lab_governance.silver;
CREATE SCHEMA lab_governance.gold;

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

CREATE TABLE lab_governance.silver.orders_clean
USING DELTA AS
SELECT order_id, customer_id, order_date, amount
FROM lab_governance.bronze.orders_raw
WHERE status = 'paid' AND amount > 0;

CREATE TABLE lab_governance.gold.daily_sales
USING DELTA AS
SELECT order_date, COUNT(*) AS order_count,
       SUM(amount) AS revenue
FROM lab_governance.silver.orders_clean
GROUP BY order_date;

SELECT * FROM lab_governance.gold.daily_sales
ORDER BY order_date;
