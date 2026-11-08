-- Notebook task: run as the engineer identity used in this lab.
-- This task reads silver only; it does not refresh the gold table.
SELECT current_user() AS run_identity;
SELECT COUNT(*) AS clean_rows, SUM(amount) AS total_amount
FROM lab_governance.silver.orders_clean;
