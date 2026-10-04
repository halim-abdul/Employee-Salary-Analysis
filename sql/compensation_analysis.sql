-- Financial analyst SQL examples for the employee salary dataset.
-- Load the enriched CSV into a table named salary_analytics_enriched.

-- 1. Executive payroll KPIs
SELECT
    COUNT(*) AS headcount,
    SUM(salary) AS total_payroll,
    AVG(salary) AS average_salary,
    MIN(salary) AS minimum_salary,
    MAX(salary) AS maximum_salary
FROM salary_analytics_enriched;

-- 2. Payroll by experience band
SELECT
    experience_band,
    COUNT(*) AS headcount,
    AVG(salary) AS average_salary,
    SUM(salary) AS payroll,
    100.0 * SUM(salary) / SUM(SUM(salary)) OVER () AS payroll_share_pct
FROM salary_analytics_enriched
GROUP BY experience_band
ORDER BY payroll DESC;

-- 3. Education / qualification compensation profile
SELECT
    degree,
    qualification,
    COUNT(*) AS headcount,
    AVG(salary) AS average_salary,
    SUM(salary) AS total_payroll
FROM salary_analytics_enriched
GROUP BY degree, qualification
ORDER BY total_payroll DESC;

-- 4. Salary increase scenario cost
SELECT
    SUM(salary) AS current_payroll,
    SUM(salary_after_3pct_raise) AS payroll_after_3pct,
    SUM(incremental_cost_3pct_raise) AS incremental_cost_3pct,
    SUM(salary_after_5pct_raise) AS payroll_after_5pct,
    SUM(incremental_cost_5pct_raise) AS incremental_cost_5pct,
    SUM(salary_after_8pct_raise) AS payroll_after_8pct,
    SUM(incremental_cost_8pct_raise) AS incremental_cost_8pct
FROM salary_analytics_enriched;

-- 5. Largest benchmark deviations for analytical review
SELECT
    *
FROM salary_analytics_enriched
WHERE benchmark_gap IS NOT NULL
ORDER BY ABS(benchmark_gap_pct) DESC;
