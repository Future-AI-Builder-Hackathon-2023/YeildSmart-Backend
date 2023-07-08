from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import pickle

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
)

cropRecomendation = pd.read_csv('./crop_prediction.csv')

better_model = pickle.load(open('./crop_prediction.pkl', 'rb'))


class cropInfo(BaseModel):
    nitrogen: int
    phosphorus: int
    potassium: int
    temperature: int
    humidity: int
    ph: int
    rainfall: int

@app.get('/')
async def welcomeCropPrediction():
    return {"result": "Welcome pridiction crop"}

@app.post('/predictCrop')
async def predictCrop(cropInfo: cropInfo):
    nitrogen_value = cropInfo.nitrogen
    phosphorus_value = cropInfo.phosphorus
    potassium_value = cropInfo.potassium
    temperature_value = cropInfo.temperature
    humidity_value = cropInfo.humidity
    ph_value = cropInfo.ph
    rainfall_value = cropInfo.rainfall

    prediction = better_model.predict(
        pd.DataFrame([[nitrogen_value, phosphorus_value, potassium_value, temperature_value, humidity_value, ph_value, rainfall_value]],
                     columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
                     ))
    print(prediction)

    return {"result": prediction[0]}
