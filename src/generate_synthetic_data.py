
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "synthetic" / "checkins.csv"


def generate_data(n_records=1000, seed=42):
    rng = np.random.default_rng(seed)

    df = pd.DataFrame({
        "record_id": [f"SYN-{i:05d}" for i in range(1, n_records + 1)],
        "sleep_hours": np.round(rng.uniform(4, 11, n_records), 1),
        "mood_rating": rng.integers(1, 6, n_records),
        "stress_rating": rng.integers(1, 6, n_records),
        "checkin_day": rng.integers(1, 31, n_records),
    })

    # Introduce a small number of missing values for testing.
    missing_indices = rng.choice(
        n_records,
        size=max(1, int(n_records * 0.03)),
        replace=False,
    )
    df.loc[missing_indices, "sleep_hours"] = np.nan

    # This is a simulated rule-based flag, NOT a clinical label.
    df["simulated_review_flag"] = (
        (df["stress_rating"] >= 4)
        & (df["mood_rating"] <= 2)
    ).astype(int)

    return df


if __name__ == "__main__":
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = generate_data()
    data.to_csv(OUTPUT_PATH, index=False)

    print(f"Synthetic dataset saved to: {OUTPUT_PATH}")
    print(f"Dataset shape: {data.shape}")
    print(data.head())
    print("\nMissing values:")
    print(data.isna().sum())
