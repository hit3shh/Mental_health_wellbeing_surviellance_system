
from pathlib import Path

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "WHO_GSHS_2022"
    / "IND-Jaipur-2022.csv"
)

TARGET = "mh_b_lonely"
FEATURES = [
    "de_age",
    "de_sex",
    "de_grade",
    "pa_sleep",
    "pf_parunderstood",
]


def evaluate_model(name, model, X_test, y_test):
    predictions = model.predict(X_test)

    print(f"\n{'=' * 50}")
    print(name)
    print("=" * 50)
    print(f"Accuracy:          {accuracy_score(y_test, predictions):.3f}")
    print(
        "Balanced accuracy: "
        f"{balanced_accuracy_score(y_test, predictions):.3f}"
    )
    print(f"Precision (Yes):   {precision_score(y_test, predictions, zero_division=0):.3f}")
    print(f"Recall (Yes):      {recall_score(y_test, predictions, zero_division=0):.3f}")
    print(f"F1-score (Yes):    {f1_score(y_test, predictions, zero_division=0):.3f}")
    print("\nConfusion matrix [actual rows, predicted columns]:")
    print(confusion_matrix(y_test, predictions, labels=[1, 0]))
    print("\nClassification report:")
    print(
        classification_report(
            y_test,
            predictions,
            labels=[1, 0],
            target_names=["Loneliness: Yes", "Loneliness: No"],
            zero_division=0,
        )
    )


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH, low_memory=False)

    required = [TARGET, *FEATURES]
    missing_columns = [col for col in required if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    # Binary codebook: 1 = Yes, 2 = No.
    # Exclude records without a target response.
    df = df.loc[df[TARGET].isin([1, 2]), required].copy()
    y = df[TARGET].map({1: 1, 2: 0}).astype(int)
    X = df[FEATURES].copy()

    print("MindWell baseline experiment")
    print(f"Usable target records: {len(df)}")
    print(f"Loneliness Yes: {(y == 1).sum()}")
    print(f"Loneliness No:  {(y == 0).sum()}")
    print(f"Features: {FEATURES}")

    # Treat numeric response codes as categories, not continuous measurements.
    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocessing = ColumnTransformer([
        ("categorical", categorical_pipeline, FEATURES),
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print(f"\nTraining records: {len(X_train)}")
    print(f"Testing records:  {len(X_test)}")

    baseline = DummyClassifier(strategy="most_frequent")
    baseline.fit(X_train, y_train)
    evaluate_model("Majority-class baseline", baseline, X_test, y_test)

    model = Pipeline([
        ("preprocessing", preprocessing),
        ("classifier", LogisticRegression(
            class_weight="balanced",
            max_iter=1000,
            random_state=42,
        )),
    ])

    model.fit(X_train, y_train)
    evaluate_model("Logistic Regression", model, X_test, y_test)

    print("\nExperiment complete. No files were saved or modified.")


if __name__ == "__main__":
    main()
