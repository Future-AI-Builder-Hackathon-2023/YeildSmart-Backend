from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import pickle

app = FastAPI()
origins = ["*"]

app.add_midleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
)

cropRecomendation = pd.read_csv('./crop_prediction.csv')

better_model = pickle.load(open('./crop_prediction.pkl','rb'))

class cropInfo(BaseModel):
    nitrogen: int
    phosphorus: int
    potassium:int
    temperature: int
    humidity: int
    ph: int
    rainfall: int