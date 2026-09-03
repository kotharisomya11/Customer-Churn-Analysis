"""
Customer Churn Analysis
Author: Harsh Pandey

Goal:
    Identify which customer segments (contract type, tenure, charges) are
    most at risk of churning, and surface retention recommendations.

Run:
    pip install pandas matplotlib
    python analysis.py
"""

import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "data/customer_churn.csv"


def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["TenureGroup"] = pd.cut(
        df["Tenure"], bins=[0, 12, 24, 36, 48, 72],
        labels=["0-12", "13-24", "25-36", "37-48", "49-72"]
    )
    return df


def overview(df: pd.DataFrame) -> None:
    churn_rate = (df["Churn"] == "Yes").mean() * 100
    print("=== Overview ===")
    print(f"Total Customers : {len(df):,}")
    print(f"Churn Rate      : {churn_rate:.1f}%")
    print(f"Avg Tenure      : {df['Tenure'].mean():.1f} months")
    print(f"Avg Monthly Chg : ${df['MonthlyCharges'].mean():.2f}\n")


def churn_by_contract(df: pd.DataFrame) -> pd.DataFrame:
    ct = pd.crosstab(df["Contract"], df["Churn"], normalize="index") * 100
    ct.plot(kind="bar", stacked=True, figsize=(7, 4.5),
            color=["#16a34a", "#dc2626"], title="Churn Rate by Contract Type")
    plt.ylabel("% of Customers")
    plt.tight_layout()
    plt.savefig("churn_by_contract.png", dpi=130)
    plt.close()
    return ct


def churn_by_tenure(df: pd.DataFrame) -> pd.DataFrame:
    tg = pd.crosstab(df["TenureGroup"], df["Churn"], normalize="index") * 100
    tg.plot(kind="bar", figsize=(7, 4.5), color=["#16a34a", "#dc2626"],
            title="Churn Rate by Tenure Group (months)")
    plt.ylabel("% of Customers")
    plt.tight_layout()
    plt.savefig("churn_by_tenure.png", dpi=130)
    plt.close()
    return tg


def charges_distribution(df: pd.DataFrame) -> None:
    plt.figure(figsize=(7, 4.5))
    df[df["Churn"] == "Yes"]["MonthlyCharges"].plot(
        kind="hist", alpha=0.6, bins=20, color="#dc2626", label="Churned")
    df[df["Churn"] == "No"]["MonthlyCharges"].plot(
        kind="hist", alpha=0.6, bins=20, color="#16a34a", label="Retained")
    plt.title("Monthly Charges Distribution: Churned vs Retained")
    plt.xlabel("Monthly Charges ($)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("charges_distribution.png", dpi=130)
    plt.close()


def main() -> None:
    df = load_data()
    overview(df)

    print("=== Churn % by Contract ===")
    print(churn_by_contract(df), "\n")

    print("=== Churn % by Tenure Group ===")
    print(churn_by_tenure(df), "\n")

    charges_distribution(df)
    print("Charts saved: churn_by_contract.png, churn_by_tenure.png, charges_distribution.png")


if __name__ == "__main__":
    main()
