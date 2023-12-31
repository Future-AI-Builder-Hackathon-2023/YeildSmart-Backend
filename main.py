from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Models.userModel import User, UserLogin
from Schemas.userSchema import users_serializer
from bson import ObjectId
from DB_Config.database import collection
from Utils.passwordHash import *
import pandas as pd
import pickle
import httpx
import requests

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.post('/createUser')
async def createUser(user: User):
    user.password = getHashPassword(user.password)
    _id = collection.insert_one(dict(user))
    user = users_serializer(collection.find({"_id": _id.inserted_id}))

    return {"status": "Ok", "data": user}


@app.post('/loginUser')
async def loginUser(userLogin: UserLogin, res: Response):
    user = users_serializer(collection.find({"email": userLogin.email}))
    if len(user) == 0:
        raise HTTPException(status_code=404, detail="User not found")
    userPassword = userLogin.password
    if verifyPassword(userPassword, user[0]['password']):
        res.status_code = 200
        return {"status": "Ok", "data": user[0]}
    raise HTTPException(status_code=404, detail="Invalid Cridential")


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
                     columns=['N', 'P', 'K', 'temperature',
                              'humidity', 'ph', 'rainfall']
                     ))
    print(prediction)

    url = "http://3.88.181.187:8080/v1/"
    search = (
        "Hey ChatGpt can u help to suggest me crop on basis of data I have in farm Nitrogn"
        + str(nitrogen_value)
        + "ppm, Phosphorous "
        + str(phosphorus_value)
        + "ppm, Potasium "
        + str(potassium_value)
        + "ppm, Temperature "
        + str(temperature_value)
        + " C, humidity "
        + str(humidity_value)
        + "%, ph "
        + str(ph_value)
        + ", rainfall "
        + str(rainfall_value)
        + "mm. Give only one-word crop name and no other details."
    )
    data = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": search}]
            }
    res = requests.post(url,json=data)

    if res.status_code == 200:
        return {"result": res.json()["choices"][0]["message"]["content"]};

    return {"result": prediction[0]}
