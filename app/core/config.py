import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
from pydantic import field_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Green Light Quiz API"
    API_V1_STR: str = "/api/v1"
    
    JWT_SECRET_KEY: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    CORS_ORIGINS: List[str] = ["*"]
     
    # By using os.getenv as the default, we ensure it checks the system first
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def fix_postgres_protocol(cls, v: Optional[str]) -> Optional[str]:
        if v and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

    # THIS IS THE KEY FIX FOR RAILWAY
    model_config = SettingsConfigDict(
        env_file=None,  
        extra="ignore"
    )

settings = Settings()