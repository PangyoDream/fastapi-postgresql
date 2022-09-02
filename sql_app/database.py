from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Settings

settings = Settings()

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:post@"+settings.postgres_db_ip+":"+settings.postgres_port+"/numanguan"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
