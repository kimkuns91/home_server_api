from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Home Server API"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    github_webhook_secret: str = ""
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/dbname"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
