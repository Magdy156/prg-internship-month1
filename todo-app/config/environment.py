from pydantic_settings import BaseSettings
from pydantic import Field
import os

def get_env_filename() -> str:
    return ".env"

class EnvironmentSettings(BaseSettings):
    # Application settings
    APP_NAME: str = Field(default="Todo App")
    APP_VERSION: str | None = None
    APP_DESCRIPTION: str | None = None
    APP_HOST: str = Field(default="0.0.0.0")
    APP_PORT: int = Field(default=8000)
    
    # JWT settings
    SECRET_KEY: str = Field(default="Default")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)
    
    # Database settings
    DATABASE_URL: str

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"
