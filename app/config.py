from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_port: str
    rds_endpoint: str
    rds_user: str
    rds_passwd: str
    bucket_name: str
    aws_access_key_id: str
    aws_secret_access_key: str
    region: str
    class Config:
        env_file = ".env"