from typing import List
from urllib.request import Request

from fastapi import Depends, FastAPI, HTTPException, Form, Body, Request, File, UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from app.config import Settings

import os
import base64
import io
from random import randrange

from PIL import Image, ImageOps
import numpy as np
import boto3

models.Base.metadata.create_all(bind=engine)
settings = Settings()


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
def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/robots.txt", response_class=FileResponse)
def robots():
    return "../robots.txt"

@app.post("/result/")
def create_user(request: Request, image: UploadFile = File() , name: str = Form(), gender: str = Form(), year: str = Form(), month: str=Form(), day: str=Form(),keyword: str=Form(), db: Session= Depends(get_db)):
        
    user = schemas.UserCreate
    user.name = name
    user.gender = gender
    user.year = year
    user.month = month
    user.day = day
    crud.create_user(db, user=user) 
    saju = crud.get_saju(db, user.gender, user.year, user.month, user.day)
    
    try:
        contents = image.file.read()
    finally:
        image.file.close()

    my_image = base64.b64encode(contents).decode("utf-8")

    ########## S3 configure & get images ########
    s3 = boto3.resource('s3', aws_access_key_id=settings.aws_access_key_id, aws_secret_access_key=settings.aws_secret_access_key, region_name=settings.region)
    bucket = s3.Bucket(settings.bucket_name)
    image_list = []

    for url in bucket.objects.all():
        if user.gender in url.key and keyword in url.key:
            image_list.append(url.key)

    fixed_image = image_list[randrange(4)]
    obj = s3.Object(settings.bucket_name, fixed_image)
    file_obj = obj.get()["Body"].read()
    f = io.BytesIO(file_obj)
    im_bytes = f.getvalue()
    other_image = base64.b64encode(im_bytes).decode("utf-8")

    return templates.TemplateResponse("result.html", {"request":request,"name":user.name, "image":my_image, "other_image":other_image, "keyword": keyword ,"look":saju.look, "personality":saju.personality})