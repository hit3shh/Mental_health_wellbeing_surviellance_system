
from pathlib import Path

import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "WHO_GSHS_2022" / "IND-Jaipur-2022.csv"

TARGET = "mh_b_lonely"

FEATURES = [
    "de_age",
    "de_sex",
    "de_grade",
    "pa_sleep",
    "pf_parunderstood",
]


def main():
    if not DATA_PATH.exists():
        print(f"Dataset not found: {DATA_PATH}")
        print("Check the dataset filename and location.")
        return

    df = pd.read_csv(DATA_PATH, low_memory=False)

    print("\n=== MINDWELL: ML DATA INSPECTION ===")
    print(f"Dataset shape: {df.shape}")
    print(f"Exact duplicate rows: {df.duplicated().sum()}")

    required = [TARGET, *FEATURES]
    missing_columns = [col for col in required if col not in df.columns]

    if missing_columns:
        print("\nMissing required columns:")
        for col in missing_columns:
            print(f"- {col}")
        return

    print("\n=== TARGET DISTRIBUTION ===")
    print("Raw target values, including missing:")
    print(df[TARGET].value_counts(dropna=False).sort_index())

    print("\n=== FEATURE SUMMARY ===")
    print(df[FEATURES].describe(include="all").T)

    print("\n=== MISSING VALUES ===")
    missing = df[required].isna().sum()
    missing_pct = (missing / len(df) * 100).round(2)

    print(pd.DataFrame({
        "missing_count": missing,
        "missing_percent": missing_pct,
    }))

    print("\n=== DISTINCT VALUES ===")
    for col in required:
        values = df[col].dropna().unique()
        print(f"\n{col}: {sorted(values.tolist(), key=str)[:30]}")

    print("\nInspection complete. No files were modified.")


if __name__ == "__main__":
    main()
