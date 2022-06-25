from fastapi import FastAPI,File,UploadFile
import uvicorn 
import numpy as np
import tensorflow as tf
from io import BytesIO
from PIL import Image
from keras.models import load_model
from flask import json


app=FastAPI()

MODEL=load_model("../training/trained_model.h5")
CLS_NAME=["Tomato_Bacterial_spot",
 "Tomato_Early_blight",
 "Tomato_Late_blight",
 "Tomato_Leaf_Mold",
 "Tomato_Septoria_leaf_spot",
 "Tomato_Spider_mites_Two_spotted_spider_mite",
 "Tomato__Target_Spot",
 "Tomato__Tomato_YellowLeaf__Curl_Virus",
 "Tomato__Tomato_mosaic_virus",
 "Tomato_healthy"]

@app.get("/ping")
async def ping():
    return "Hello Hello"

def file_to_image(data):
    image=np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
     file: UploadFile =File(...)
):
    image= file_to_image(await file.read())
    
    img_batch=np.expand_dims(image,0)
    prediction=MODEL.predict(img_batch)
     
    cls=CLS_NAME[np.argmax(prediction[0])]
    confidence=np.max(prediction[0])
    return {
        'class':cls,
        'confidence': float(confidence)
    }

if __name__=="__main__":
    uvicorn.run(app,host='localhost',port=3001)