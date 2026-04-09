import os
import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from config import MODEL_PATH


FEATURE_COLUMNS = [
    "status_changed",
    "length_diff_ratio",
    "response_time_diff",
    "sql_error_count",
    "payload_reflected",
    "redirect_changed",
    "diff_ratio"
]


def train_model(feature_rows):
    os.makedirs("data", exist_ok=True)

    if not feature_rows:
        raise ValueError("No baseline feature rows were collected. Check crawler output and endpoint parameters.")

    df = pd.DataFrame(feature_rows)

    for col in FEATURE_COLUMNS:
        if col not in df.columns:
            df[col] = 0

    df = df[FEATURE_COLUMNS]

    print("\n[DEBUG] Training DataFrame:")
    print(df.head())
    print("[DEBUG] Training rows:", len(df))

    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(df)

    joblib.dump(model, MODEL_PATH)
    df.to_csv("data/baseline_features.csv", index=False)
    print("[INFO] Model and baseline CSV saved successfully")


def load_model():
    return joblib.load(MODEL_PATH)


def predict_anomaly(model, feature_dict):
    df = pd.DataFrame([feature_dict])

    for col in FEATURE_COLUMNS:
        if col not in df.columns:
            df[col] = 0

    df = df[FEATURE_COLUMNS]

    pred = model.predict(df)[0]
    score = model.decision_function(df)[0]

    anomaly_label = 1 if pred == -1 else 0
    anomaly_score = max(0.0, min(1.0, 1 - (score + 0.5)))

    return {
        "anomaly_label": anomaly_label,
        "anomaly_score": anomaly_score
    }