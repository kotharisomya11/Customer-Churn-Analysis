-- =====================================================================
-- Customer Churn Analysis — SQL Queries
-- Author: Harsh Pandey
-- Table assumed: customer_churn (loaded from data/customer_churn.csv)
-- =====================================================================

-- 1. Overall churn rate
SELECT
    COUNT(*)                                              AS total_customers,
    SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END)          AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS churn_rate_pct
FROM customer_churn;


-- 2. Churn rate by contract type
SELECT
    Contract,
    COUNT(*)                                              AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS churn_rate_pct
FROM customer_churn
GROUP BY Contract
ORDER BY churn_rate_pct DESC;


-- 3. Churn rate by tenure bucket
SELECT
    CASE
        WHEN Tenure <= 12 THEN '0-12'
        WHEN Tenure <= 24 THEN '13-24'
        WHEN Tenure <= 36 THEN '25-36'
        WHEN Tenure <= 48 THEN '37-48'
        ELSE '49-72'
    END AS tenure_group,
    COUNT(*)                                              AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS churn_rate_pct
FROM customer_churn
GROUP BY tenure_group
ORDER BY tenure_group;


-- 4. Churn rate by internet service type
SELECT
    InternetService,
    COUNT(*)                                              AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS churn_rate_pct
FROM customer_churn
GROUP BY InternetService
ORDER BY churn_rate_pct DESC;


-- 5. Average monthly charges: churned vs retained
SELECT
    Churn,
    ROUND(AVG(MonthlyCharges), 2)                         AS avg_monthly_charges,
    ROUND(AVG(TotalCharges), 2)                           AS avg_total_charges,
    ROUND(AVG(Tenure), 1)                                 AS avg_tenure
FROM customer_churn
GROUP BY Churn;


-- 6. Highest-risk segment: contract + payment method combo
SELECT
    Contract,
    PaymentMethod,
    COUNT(*)                                              AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS churn_rate_pct
FROM customer_churn
GROUP BY Contract, PaymentMethod
HAVING COUNT(*) >= 15
ORDER BY churn_rate_pct DESC
LIMIT 5;
