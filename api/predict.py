import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from utils.utils import get_lat_lng

MODEL_PATH = Path(__file__).parent / "model" / "xgboost_model.joblib"

model = joblib.load(MODEL_PATH)

MODEL_FEATURE_COLS = model.named_steps["preprocessor"].feature_names_in_

def predict(data: dict) -> float:
    """
    Take a single property's raw feature dict, extracts inputs for model input, 
    reverse-logs the prediction and return predicted price.
    """
    data = get_lat_lng(data)
    model_input = {k: v for k, v in data.items() if k in MODEL_FEATURE_COLS}
    df = pd.DataFrame([model_input])
    log_prediction = model.predict(df)[0]
    prediction = np.expm1(log_prediction)
    return float(prediction)
    