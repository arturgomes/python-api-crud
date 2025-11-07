"""
Configuration module for the Python CRUD API.

This module uses Pydantic Settings to manage configuration from environment variables.
Similar to Rust's dotenv + config patterns, but with automatic validation.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Pydantic automatically:
    - Loads from .env file
    - Validates types
    - Provides defaults
    - Converts strings to appropriate types

    Compare to Rust:
    - Like using dotenv + serde for config
    - Type-safe at runtime (Pydantic validates)
    - No macros needed, just type hints
    """

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://pythonuser:pythonpass@localhost:5433/pythoncrud"

    # Application
    APP_NAME: str = "Python CRUD API"
    APP_VERSION: str = "0.1.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Pydantic Settings configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# Global settings instance
# Similar to lazy_static! in Rust - single global configuration
settings = Settings()
