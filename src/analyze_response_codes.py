
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "raw" / "changing_childhood.csv"
OUTPUT_PATH = ROOT / "docs" / "datasets" / "response_frequency_report.csv"

df = pd.read_csv(DATA_PATH, low_memory=False)

# Coded survey variables to inspect first.
columns_to_check = [
    "EMP_2010", "EMP_FTEMP", "EMP_LFPR", "EMP_WORK_HOURS",
    "WP10200", "WP10202", "WP12", "WP1220", "WP1219",
    "WP1230RECODED", "WP1233RECODED", "WP16056", "WP2319",
    "WP30", "WP3117", "WP40", "WP4657",
    "WP22827", "WP22086", "WP22087", "WP22088",
    "WP22089", "WP22090", "WP22091", "WP22125",
    "WP22826", "WP22828"
]

rows = []

for col in columns_to_check:
    if col not in df.columns:
        continue

    counts = df[col].value_counts(dropna=False).sort_index()

    for value, count in counts.items():
        rows.append({
            "column": col,
            "raw_value": "MISSING" if pd.isna(value) else value,
            "count": int(count),
            "percentage": round(count / len(df) * 100, 2)
        })

report = pd.DataFrame(rows)
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
report.to_csv(OUTPUT_PATH, index=False)

print("Report saved:", OUTPUT_PATH)
print(report.to_string(index=False))
