from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from app.predict import predict_url
from fastapi.middleware.cors import CORSMiddleware

from PIL import Image
import cv2
import numpy as np
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

# ---------- HOME ----------
@app.get("/")
def home():
    return {"message": "NEXRA API Running"}

# ---------- URL PREDICT ----------
@app.post("/predict")
def predict(data: URLRequest):

    if not data.url.startswith("http"):
        return {"error": "Invalid URL"}

    result = predict_url(data.url)

    return {
        "result": result
    }

# ---------- QR FUNCTION ----------
def extract_qr_data(image):
    try:
        # Convert to RGB (IMPORTANT)
        image = image.convert("RGB")

        # Convert to numpy array
        image = np.array(image)

        # Ensure correct type
        if image is None or image.size == 0:
            return None

        # Convert color
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(image)

        if data:
            return data

        return None

    except Exception as e:
        print("QR ERROR:", e)
        return None

# ---------- QR API ----------
@app.post("/predict_qr")
async def predict_qr(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        url = extract_qr_data(image)

        print("QR URL:", url)  # ✅ correct place

        if not url:
            return {"error": "No QR code found"}

        result = predict_url(url)

        return {
            "extracted_url": url,   # ✅ FIXED KEY
            "prediction": result
        }

    except Exception as e:
        return {"error": str(e)}