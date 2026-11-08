-- Run as the catalog/table owner or another authorized lab administrator.
-- Account groups lab_engineers and lab_analysts must already exist.
GRANT USE CATALOG ON CATALOG lab_governance
TO `lab_engineers`;
GRANT USE SCHEMA ON SCHEMA lab_governance.bronze
TO `lab_engineers`;
GRANT USE SCHEMA ON SCHEMA lab_governance.silver
TO `lab_engineers`;
GRANT CREATE TABLE ON SCHEMA lab_governance.silver
TO `lab_engineers`;

GRANT SELECT, MODIFY
ON TABLE lab_governance.bronze.orders_raw
TO `lab_engineers`;
GRANT SELECT, MODIFY
ON TABLE lab_governance.silver.orders_clean
TO `lab_engineers`;

GRANT USE CATALOG ON CATALOG lab_governance
TO `lab_analysts`;
GRANT USE SCHEMA ON SCHEMA lab_governance.gold
TO `lab_analysts`;
GRANT SELECT ON TABLE lab_governance.gold.daily_sales
TO `lab_analysts`;

SHOW GRANTS ON CATALOG lab_governance;
SHOW GRANTS ON SCHEMA lab_governance.gold;
SHOW GRANTS ON TABLE lab_governance.gold.daily_sales;
