-- Run EACH statement separately as a non-admin lab_analysts member.
-- Expected: permission errors, not result sets.
SELECT * FROM lab_governance.bronze.orders_raw;

-- A no-match predicate avoids changing sample data if grants are too broad.
DELETE FROM lab_governance.gold.daily_sales
WHERE order_date = DATE '1900-01-01';

CREATE TABLE lab_governance.gold.analyst_probe (id INT);
