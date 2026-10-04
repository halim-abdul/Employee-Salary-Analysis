"""Advanced employee compensation analysis for financial analysts.

The script is intentionally tolerant of common salary dataset column names.
It produces clean BI-ready tables in outputs/.
"""
from pathlib import Path
import re
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "salaries.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(s).strip().lower()).strip("_")


def pick(columns, *candidates):
    lookup = {slug(c): c for c in columns}
    for c in candidates:
        if slug(c) in lookup:
            return lookup[slug(c)]
    return None


def main():
    df = pd.read_csv(DATA)
    df.columns = [slug(c) for c in df.columns]

    salary = pick(df.columns, "salary", "annual_salary", "salary_usd", "income", "pay")
    exp = pick(df.columns, "experience", "years_experience", "experience_years", "years_of_experience")
    age = pick(df.columns, "age")
    degree = pick(df.columns, "degree", "education", "education_level")
    qual = pick(df.columns, "qualification", "qualifications")

    if salary is None:
        raise ValueError("No salary/pay column found. Rename the salary field to salary or annual_salary.")

    # Financial hygiene
    df[salary] = pd.to_numeric(df[salary], errors="coerce")
    if age: df[age] = pd.to_numeric(df[age], errors="coerce")
    if exp: df[exp] = pd.to_numeric(df[exp], errors="coerce")
    df = df.dropna(subset=[salary]).copy()
    df = df[df[salary] >= 0]

    # Core compensation metrics
    q1, med, q3 = df[salary].quantile([0.25, 0.50, 0.75])
    mean_salary = df[salary].mean()
    p10, p90 = df[salary].quantile([0.10, 0.90])
    payroll = df[salary].sum()
    kpis = pd.DataFrame({
        "metric": ["headcount", "total_payroll", "average_salary", "median_salary", "p10_salary", "p90_salary", "salary_q1", "salary_q3", "payroll_per_employee"],
        "value": [len(df), payroll, mean_salary, med, p10, p90, q1, q3, payroll / len(df)]
    })
    kpis.to_csv(OUT / "finance_kpis.csv", index=False)

    # Pay-band / quartile framework for workforce planning
    df["salary_percentile"] = df[salary].rank(pct=True)
    df["pay_band"] = pd.cut(df["salary_percentile"], bins=[0, .25, .50, .75, 1.0], labels=["Q1-Low", "Q2", "Q3", "Q4-High"], include_lowest=True)
    df["salary_vs_median_pct"] = np.where(med != 0, (df[salary] / med - 1) * 100, np.nan)
    df["salary_vs_mean_pct"] = np.where(mean_salary != 0, (df[salary] / mean_salary - 1) * 100, np.nan)

    # Age and experience bands aid cohort analysis in Power BI/Tableau
    if age:
        df["age_band"] = pd.cut(df[age], bins=[0,24,34,44,54,64,200], labels=["<25","25-34","35-44","45-54","55-64","65+"])
    if exp:
        df["experience_band"] = pd.cut(df[exp], bins=[-1,2,5,10,15,25,1e9], labels=["0-2","3-5","6-10","11-15","16-25","25+"])

    dimensions = [c for c in [degree, qual, "pay_band", "age_band", "experience_band"] if c and c in df.columns]
    summaries = []
    for dim in dimensions:
        g = df.groupby(dim, observed=True)[salary].agg(headcount="size", avg_salary="mean", median_salary="median", total_payroll="sum", min_salary="min", max_salary="max").reset_index()
        g["dimension"] = dim
        g = g.rename(columns={dim: "segment"})
        summaries.append(g)
    if summaries:
        pd.concat(summaries, ignore_index=True).to_csv(OUT / "segment_compensation_summary.csv", index=False)

    # Simple salary driver model: useful for analytical benchmarking, not HR decision automation.
    features = [c for c in [exp, age, degree, qual] if c]
    if features and len(df) >= 30:
        X = df[features].copy()
        y = df[salary]
        numeric = [c for c in features if pd.api.types.is_numeric_dtype(X[c])]
        categorical = [c for c in features if c not in numeric]
        prep = ColumnTransformer([
            ("num", "passthrough", numeric),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ])
        model = Pipeline([("prep", prep), ("model", LinearRegression())])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        pd.DataFrame({
            "metric": ["MAE", "R2"],
            "value": [mean_absolute_error(y_test, pred), r2_score(y_test, pred)]
        }).to_csv(OUT / "salary_model_metrics.csv", index=False)

        df["benchmark_salary"] = model.predict(X)
        df["benchmark_gap"] = df[salary] - df["benchmark_salary"]
        df["benchmark_gap_pct"] = np.where(df["benchmark_salary"] != 0, df["benchmark_gap"] / df["benchmark_salary"] * 100, np.nan)

    # Scenario fields for finance planning
    for pct in (3, 5, 8):
        df[f"salary_after_{pct}pct_raise"] = df[salary] * (1 + pct / 100)
        df[f"incremental_cost_{pct}pct_raise"] = df[salary] * pct / 100

    df.to_csv(OUT / "salary_analytics_enriched.csv", index=False)
    print(f"Wrote analysis outputs to {OUT}")


if __name__ == "__main__":
    main()
