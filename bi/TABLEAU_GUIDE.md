# Tableau Dashboard Guide

Connect Tableau to `outputs/salary_analytics_enriched.csv`.

## Dashboard 1 — Compensation Executive Summary

**KPI cards**
- Employee headcount
- Total annual payroll
- Average salary
- Median salary
- P10 and P90 salary
- Payroll per employee

**Views**
- Salary distribution
- Pay-band composition
- Payroll contribution by pay band
- Average/median salary by qualification

## Dashboard 2 — Salary Drivers

Recommended worksheets:
- Experience vs salary scatter plot with trend line
- Salary box plot by degree
- Salary box plot by qualification
- Median salary heatmap: experience band × degree
- Age band vs median salary

Useful parameters:
- Metric selector: Average / Median / Total Payroll
- Salary increase scenario: 0%, 3%, 5%, 8%

## Dashboard 3 — Financial Planning

Create calculated fields:

```text
Scenario Salary
CASE [Raise Scenario]
WHEN "0%" THEN [salary]
WHEN "3%" THEN [salary_after_3pct_raise]
WHEN "5%" THEN [salary_after_5pct_raise]
WHEN "8%" THEN [salary_after_8pct_raise]
END
```

```text
Scenario Incremental Cost
[Scenario Salary] - [salary]
```

Show:
- Current payroll vs scenario payroll
- Incremental annual and monthly payroll cost
- Incremental cost by degree / qualification / experience band
- Waterfall-style view of payroll growth across cohorts

## Dashboard 4 — Benchmark Diagnostics

Use:
- `benchmark_salary`
- `benchmark_gap`
- `benchmark_gap_pct`

Recommended charts:
- Actual vs benchmark scatter
- Gap % distribution
- Gap by experience band
- Gap by qualification

The benchmark is an analytical model for understanding dataset structure. It should not be treated as an automated HR, hiring, promotion, or compensation decision system.

## Story points for a portfolio presentation

1. Workforce compensation structure
2. Education and experience effects
3. Financial impact of salary adjustments
4. Analytical benchmark diagnostics
5. Management recommendations and data limitations
