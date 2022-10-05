from sqlalchemy.orm import Session

from sql_app import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_saju(db: Session, gender: str, year: int, month: int, day: int):
    return db.query(models.Saju).filter(models.Saju.gender == gender
    , models.Saju.year == year, models.Saju.month == month
    , models.Saju.day == day).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, gender=user.gender, year=user.year, month=user.month, day=user.day)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
