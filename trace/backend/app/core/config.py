from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    # App
    APP_NAME: str = "T.R.A.C.E."
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://trace_user:trace_pass@localhost:5432/trace_db"
    DATABASE_SYNC_URL: str = "postgresql://trace_user:trace_pass@localhost:5432/trace_db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    SECRET_KEY: str = "supersecret-jwt-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: str = '["http://localhost:3000"]'

    # File uploads
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB

    # Geo-fencing radius in meters
    GEOFENCE_RADIUS_METERS: float = 500.0

    # AI Stubs — set real endpoints here when available
    GEM_PORTAL_BASE_URL: str = "https://gem.gov.in/api"  # MOCK — not a real endpoint
    UIDAI_API_URL: str = "https://uidai.gov.in/api"       # MOCK — not a real endpoint

    @property
    def cors_origins_list(self) -> List[str]:
        return json.loads(self.CORS_ORIGINS)

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
