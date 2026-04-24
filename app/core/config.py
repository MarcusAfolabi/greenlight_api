import os
from pydantic_settings import BaseSettings
from typing import List, Optional
from pydantic import field_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Green Light Quiz API"
    API_V1_STR: str = "/api/v1"
    
    JWT_SECRET_KEY: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    CORS_ORIGINS: List[str] = ["*"]
     
    # Use Optional and no default string to force Pydantic 
    # to look at the environment variables
    DATABASE_URL: Optional[str] = None

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def fix_postgres_protocol(cls, v: Optional[str]) -> Optional[str]:
        if v and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

    class Config:  
        env_file = ".env"
        extra = "ignore" # Ignores extra variables in the env

settings = Settings()