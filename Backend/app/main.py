from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import io
from PIL import Image
from .services import prediction

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Dog Breed Identification API!"}

@app.post("/predict", tags=["Prediction"])
async def predict_breed(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        breed = prediction.predict_dog_breed(image)
        return {"breed": breed}

    except Exception as e:
        print(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="There was an error processing the image.")
    
    