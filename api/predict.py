import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "xgboost_model.joblib"

model = joblib.load(MODEL_PATH)

def predict(data: dict) -> float:
    """Take a single property's raw feature dict, return predicted price."""
    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return float(prediction)