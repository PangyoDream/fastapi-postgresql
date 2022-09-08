from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import Settings

settings = Settings()

SQLALCHEMY_DATABASE_URL = "postgresql://"+settings.rds_user+":"+settings.rds_passwd+"@"+settings.rds_endpoint+":"+settings.postgres_port+"/numanguan"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:post@132.145.87.41:5432/numanguan"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
