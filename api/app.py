from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from schemas import PropertyInput
from predict import predict

app = FastAPI(title="Immo Eliza Price Prediction API")

@app.get("/")
def read_root():
    return "alive"

@app.post("/predict")
def predict_price(input_data: PropertyInput):
    try:
        prediction = predict(input_data.model_dump())
    except (ValueError, KeyError) as e:
        raise HTTPException(status_code=422, detail=f"Invalid input data: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal prediction error")

    return {"prediction": prediction, "status_code": 200}