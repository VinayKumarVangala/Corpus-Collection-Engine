import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_VERSION = os.getenv("API_VERSION", "v1")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

# Authentication
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
OTP_EXPIRY_MINUTES = int(os.getenv("OTP_EXPIRY_MINUTES", "5"))
SESSION_TIMEOUT_HOURS = int(os.getenv("SESSION_TIMEOUT_HOURS", "24"))

# File Upload Configuration
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE_MB", "1")) * 1024 * 1024
MAX_FILE_SIZE = {
    "text": int(os.getenv("MAX_TEXT_SIZE_KB", "200")) * 1024,
    "image": int(os.getenv("MAX_IMAGE_SIZE_MB", "10")) * 1024 * 1024,
    "audio": int(os.getenv("MAX_AUDIO_SIZE_MB", "25")) * 1024 * 1024,
    "video": int(os.getenv("MAX_VIDEO_SIZE_MB", "100")) * 1024 * 1024,
}

# Security
BCRYPT_ROUNDS = int(os.getenv("BCRYPT_ROUNDS", "12"))

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# UI Configuration
CATEGORIES_PER_ROW = 4
DASHBOARD_RECENT_LIMIT = 5