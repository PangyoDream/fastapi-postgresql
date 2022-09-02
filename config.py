from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_db_ip: str
    postgres_port: str

    class Config:
        env_file = ".env"
