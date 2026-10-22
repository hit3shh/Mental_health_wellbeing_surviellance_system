
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "changing_childhood.csv"

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_PATH}\n"
        "Place changing_childhood.csv inside data/raw/."
    )

df = pd.read_csv(DATA_PATH, low_memory=False)

print("\n--- DATASET OVERVIEW ---")
print("Shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

print("\n--- FIRST FIVE ROWS ---")
print(df.head().to_string())

print("\n--- DATA TYPES ---")
print(df.dtypes.to_string())

print("\n--- MISSING VALUES ---")
print(df.isna().sum().to_string())

print("\n--- DUPLICATE ROWS ---")
print(df.duplicated().sum())

print("\n--- NUMERIC SUMMARY ---")
print(df.describe(include="number").to_string())


from pathlib import Path
import pandas as pd

root = Path(__file__).resolve().parent.parent
df = pd.read_csv(root / "data/raw/changing_childhood.csv",
                 low_memory=False)

for col in df.columns:
    print(f"\n--- {col} ---")
    print(df[col].value_counts(dropna=False).head(12))
