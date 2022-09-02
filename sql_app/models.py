from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from sql_app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    gender = Column(String,  index=True)
    year = Column(Integer,  index=True)
    month = Column(Integer,  index=True)
    day = Column(Integer,  index=True)

class Saju(Base):
    __tablename__ = "saju"

    owner_id = Column(Integer, ForeignKey("users.id"))
    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String, index=True)
    year = Column(Integer, index=True)
    month = Column(Integer, index=True)
    day = Column(Integer,  index=True)
    look = Column(String(512), index=True)
    personality = Column(String(512), index=True)
    
    # owner_gender = Column(String, ForeignKey("users.gender"))
