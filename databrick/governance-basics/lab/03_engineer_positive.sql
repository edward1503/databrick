-- Sign in as a non-admin member of lab_engineers.
SELECT current_user();
SELECT COUNT(*) AS raw_rows
FROM lab_governance.bronze.orders_raw;
SELECT COUNT(*) AS clean_rows
FROM lab_governance.silver.orders_clean;

-- Exercise MODIFY without changing the example's values.
UPDATE lab_governance.silver.orders_clean
SET amount = amount
WHERE order_id = 'o1001';

CREATE TABLE lab_governance.silver.engineer_probe
USING DELTA AS
SELECT * FROM lab_governance.silver.orders_clean
LIMIT 1;

-- The creating user owns this probe table.
DROP TABLE lab_governance.silver.engineer_probe;
