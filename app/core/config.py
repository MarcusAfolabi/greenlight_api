import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Green Light Quiz API"
    API_V1_STR: str = "/api/v1"
    
    # JWT
    JWT_SECRET_KEY: str = "CMtF1vROVyW06LkAeKRs-yzGRHKcbs14czhq2zFxvaQ"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000", "https://greenlight-quiz.vercel.app"]
     
    DATABASE_URL: str = ""
    
    class Config: 
        env_file = os.getenv("ENV_FILE", ".env")
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()