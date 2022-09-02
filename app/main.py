from typing import List
from urllib.request import Request

from fastapi import Depends, FastAPI, HTTPException, Form, Body, Request, File, UploadFile
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import os
import base64
import io

from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/result/")
async def create_user(request: Request, image: UploadFile = File() , name: str = Form(), gender: str = Form(), year: str = Form(), month: str=Form(), day: str=Form(), db: Session= Depends(get_db)):
    print(name,gender,year,month,day)
    user = schemas.UserCreate
    user.name = name
    user.gender = gender
    user.year = year
    user.month = month
    user.day = day
    crud.create_user(db, user=user) 
    saju = crud.get_saju(db, user.gender, user.year, user.month, user.day)

    filename = image.filename
    content_type = image.content_type
    print(filename, content_type)
    # print(image)
    
    try:
        contents = image.file.read()
    finally:
        image.file.close()

    print(type(contents))
    base64_encoded_image = base64.b64encode(contents).decode("utf-8")
    print(type(base64_encoded_image))
    # Load the model
    if user.gender == '남자':
        model = load_model('model/keras_model_man.h5')
    else:
        model = load_model('model/keras_model_woman.h5')

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # Replace this with the path to your image
    image = Image.open(io.BytesIO(contents))
    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    print(prediction)

    base_dir = "images/"

    keyword = {0:"강아지상",1:"고양이상",2:"토끼상",3:"곰상", 4:"공룡상"}

    user_keyword = keyword[np.argmax(prediction)]
    other_image_dir = base_dir+user.gender+'/'+user_keyword+'/'+os.listdir(base_dir+user.gender+'/'+user_keyword)[0]

    img = Image.open(other_image_dir)

    im_file = io.BytesIO()
    img.save(im_file, format="JPEG")
    im_bytes = im_file.getvalue()
    im_b64 = base64.b64encode(im_bytes).decode("utf-8")

    return templates.TemplateResponse("result.html", {"request":request,"name":user.name, "image":base64_encoded_image, "other_image":im_b64, "keyword": user_keyword ,"look":saju.look, "personality":saju.personality})