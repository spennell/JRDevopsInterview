import sys
from pathlib import Path
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    REDIS_HOST: str = Field(..., env="REDIS_HOST")
    REDIS_DB: int = Field(..., env="REDIS_DB")
    REDIS_PORT: int = Field(..., env="REDIS_PORT")
    REDIS_QUEUE: str = Field(..., env="REDIS_QUEUE")

    class Config:
        path = f"{Path(__file__).parents[1]}/app"
        env_file = f"{path}/.env"
        env_file_encoding = 'utf-8'
        case_sensitive = True


settings = Settings()
