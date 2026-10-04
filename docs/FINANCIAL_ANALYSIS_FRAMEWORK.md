# Financial Analysis Framework

This project treats employee compensation as a workforce-cost and management-reporting problem rather than only a machine-learning exercise.

## 1. Core questions

- What is the current annual payroll obligation?
- What are average, median, P10, P90 and quartile salaries?
- How concentrated is payroll across low/mid/high compensation bands?
- How do experience, age, degree and qualification relate to compensation?
- Which employee cohorts contribute most to payroll expense?
- What is the financial impact of broad 3%, 5% and 8% salary increases?
- How far does an employee's salary deviate from a simple analytical benchmark based on observable fields?

## 2. Financial KPIs

### Payroll

`Total Payroll = sum(employee salary)`

### Payroll per employee

`Payroll per Employee = Total Payroll / Headcount`

### Salary spread

Use median, quartiles, P10 and P90 to reduce dependence on outliers.

### Payroll concentration

Compare headcount share and payroll share by pay band. A small upper-pay cohort may account for a disproportionately large percentage of salary expense.

### Raise scenario cost

For an across-the-board increase `r`:

`Incremental Payroll Cost = Current Payroll × r`

The project calculates 3%, 5%, and 8% scenarios at employee level so results can also be sliced by degree, qualification, age and experience.

## 3. Analytical benchmarking

A linear regression model uses available numeric and categorical features to estimate a dataset-implied salary benchmark. Outputs include:

- benchmark salary
- absolute gap
- percentage gap
- MAE
- R²

This is intended for exploratory financial diagnostics and model interpretation. It is not an automated HR decision engine and should not be used alone to determine hiring, promotion, termination or individual compensation.

## 4. Data quality controls

Recommended validation checks:

- duplicate employee rows
- missing salary values
- negative or impossible salaries
- impossible ages or experience values
- inconsistent degree / qualification labels
- extreme salary outliers
- currency consistency
- annual vs monthly salary consistency

## 5. Management interpretation

A financial analyst should distinguish:

- **cost observation**: what the current payroll structure is;
- **driver analysis**: which variables are associated with salary differences;
- **scenario planning**: how policy changes affect payroll;
- **benchmarking**: how actual compensation differs from a statistical baseline;
- **decision context**: business, labor-market, legal and HR factors not represented in the dataset.

## 6. BI deployment

Power BI and Tableau can consume the enriched CSV directly. Recommended executive dashboards include payroll KPIs, salary distributions, experience/education cohorts, raise scenarios, and benchmark-gap diagnostics.
