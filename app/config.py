from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_db_ip: str = "132.145.87.41"
    postgres_port: str = "5432"

    # class Config:
    #     env_file = ".env"
