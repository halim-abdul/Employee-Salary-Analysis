# Power BI Dashboard Guide

Use `outputs/salary_analytics_enriched.csv` as the main fact table and `outputs/segment_compensation_summary.csv` for executive summaries.

## Recommended pages

1. **Executive Compensation Overview**
   - Headcount
   - Total payroll
   - Average salary
   - Median salary
   - P10 / P90 salary
   - Payroll per employee
   - Salary distribution histogram
   - Pay-band headcount and payroll share

2. **Experience & Education Analysis**
   - Average salary by experience band
   - Salary vs experience scatter plot
   - Salary by degree / qualification
   - Median salary by degree and experience band
   - Decomposition Tree: salary -> degree -> qualification -> experience band -> age band

3. **Financial Planning / Raise Scenarios**
   - Current payroll
   - Payroll after 3%, 5%, 8% raise
   - Incremental annual cost
   - Incremental monthly cost
   - Raise cost by employee segment

4. **Benchmark & Exception Analysis**
   - Actual salary vs analytical benchmark
   - Benchmark gap and gap %
   - Employees/segments materially above or below model benchmark
   - Important: use this only as an analytical diagnostic, not as an automated compensation decision rule.

## Suggested DAX measures

```DAX
Headcount = COUNTROWS('salary_analytics_enriched')

Total Payroll = SUM('salary_analytics_enriched'[salary])

Average Salary = AVERAGE('salary_analytics_enriched'[salary])

Median Salary = MEDIAN('salary_analytics_enriched'[salary])

Payroll per Employee = DIVIDE([Total Payroll], [Headcount])

Payroll After 5% Raise =
SUM('salary_analytics_enriched'[salary_after_5pct_raise])

Incremental Cost 5% =
SUM('salary_analytics_enriched'[incremental_cost_5pct_raise])

Average Benchmark Gap =
AVERAGE('salary_analytics_enriched'[benchmark_gap])
```

If your salary column has a different source name, the Python pipeline normalizes the analytical exports while retaining the dataset structure. Adjust the DAX field reference if required.

## Filters / slicers

- Degree
- Qualification
- Age band
- Experience band
- Pay band

## Financial analyst questions answered

- What is the total annual salary obligation?
- Which cohorts drive the largest payroll cost?
- How concentrated is compensation in the upper salary quartile?
- What is the cost of a 3%, 5%, or 8% broad salary increase?
- How does experience correlate with salary?
- Which education/qualification cohorts have the highest median compensation?
- Where are the largest benchmark gaps?
