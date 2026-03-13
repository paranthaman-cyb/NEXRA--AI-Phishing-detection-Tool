from fastapi import FastAPI
from pydantic import BaseModel
from app.predict import predict_url




app = FastAPI() #title="NEXRA Phishing Detection API"

class URLRequest(BaseModel):
    url:str


@app.get("/")
def home():
    return {"message":"NEXRA API Running"}


@app.post("/predict")
def predict(data:URLRequest):

    result = predict_url(data.url)

    return result