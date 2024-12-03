import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Meal Planner"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./test.db" if os.getenv("ENVIRONMENT") != "production" else None
    )
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 