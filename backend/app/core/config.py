"""
Application configuration and settings.

Centralizes all environment-based configuration so that
routers, services, and models import from a single source.
"""

import os


# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sentinellab.db")

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Application
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
APP_NAME = "SentinelLab"
APP_VERSION = "0.1.0"
