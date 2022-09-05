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

# from keras.models import load_model
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
# @app.post("/result")
# async def return_result(request : Request, image: UploadFile = File(), keyword: str=Form()):
#     try:
#         contents = image.file.read()
#     finally:
#         image.file.close()

#     print(type(contents))
#     base64_encoded_image = base64.b64encode(contents).decode("utf-8")

#     return templates.TemplateResponse("result.html", {"request":request, "image": base64_encoded_image})
@app.post("/result/")
async def create_user(request: Request, image: UploadFile = File() , name: str = Form(), gender: str = Form(), year: str = Form(), month: str=Form(), day: str=Form(),keyword: str=Form(), db: Session= Depends(get_db)):
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

    base_dir = "images/"

    keyword_list = {0:"강아지상",1:"고양이상",2:"토끼상",3:"곰상", 4:"공룡상"}
    print(keyword)

    # user_keyword = keyword_list[np.argmax(prediction)]
    other_image_dir = base_dir+user.gender+'/'+keyword+'/'+os.listdir(base_dir+user.gender+'/'+keyword)[0]

    img = Image.open(other_image_dir)

    im_file = io.BytesIO()
    img.save(im_file, format="JPEG")
    im_bytes = im_file.getvalue()
    im_b64 = base64.b64encode(im_bytes).decode("utf-8")

    return templates.TemplateResponse("result.html", {"request":request,"name":user.name, "image":base64_encoded_image, "other_image":im_b64, "keyword": keyword ,"look":saju.look, "personality":saju.personality})