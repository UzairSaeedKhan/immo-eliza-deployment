from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from schemas import PropertyInput
from predict import predict
from logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI(title="Immo Eliza Price Prediction API")

@app.get("/")
def read_root():
    return "alive"

@app.post("/predict")
def predict_price(input_data: PropertyInput):
    try:
        prediction = predict(input_data.model_dump())
    except (ValueError, KeyError) as e:
        logger.warning(f"Invalid input: {e}")
        raise HTTPException(status_code=422, detail=f"Invalid input data: {e}")
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Internal prediction error")

    return {"prediction": prediction, "status_code": 200}