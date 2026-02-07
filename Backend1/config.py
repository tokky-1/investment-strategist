"""
config.py
Centralized Configuration Management

Loads environment variables and provides app-wide settings.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Uses pydantic for validation and type safety.
    """
    
    # API Keys
    gemini_api_key: str = "AIzaSyDXe5-IQN_-kNjg5zvlQqd2W9S4lJaCyhg"
    finnhub_api_key: str = "d608fjpr01qihi8os6lgd608fjpr01qihi8os6m0"
    exchange_rate_api_key: str = "fee4608d54e91c215b983be7"
    
    # Application Settings
    app_name: str = "Intelligent Investment Strategist API"
    app_version: str = "1.0.0"
    app_env: str = "development"
    debug: bool = True
    
    # Server Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # CORS Settings
    frontend_url: str = "http://localhost:5173"
    allowed_origins: list = ["*"]  # In production, use specific URLs
    
    # File Upload Settings
    max_file_size: int = 10 * 1024 * 1024  # 10 MB
    allowed_pdf_extensions: list = [".pdf"]
    allowed_audio_extensions: list = [".mp3", ".wav", ".m4a", ".ogg", ".flac"]
    
    # API Rate Limiting (optional, for future implementation)
    rate_limit_per_minute: int = 60
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to avoid reloading .env file on every call.
    """
    return Settings()


# Convenience function to get specific settings
def get_api_keys():
    """Get all API keys as a dictionary"""
    settings = get_settings()
    return {
        "gemini": settings.gemini_api_key,
        "finnhub": settings.finnhub_api_key,
        "exchange_rate": settings.exchange_rate_api_key
    }


def is_production() -> bool:
    """Check if running in production environment"""
    settings = get_settings()
    return settings.app_env.lower() == "production"


def is_debug_mode() -> bool:
    """Check if debug mode is enabled"""
    settings = get_settings()
    return settings.debug


# Export settings instance
settings = get_settings()
