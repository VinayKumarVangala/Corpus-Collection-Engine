import os
from pathlib import Path

# App Configuration
APP_NAME = "Corpus Collection Engine"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# File Upload Limits (as per SRD)
MAX_FILE_SIZES = {
    "text": 200 * 1024,  # 200KB
    "image": 10 * 1024 * 1024,  # 10MB
    "audio": 25 * 1024 * 1024,  # 25MB
    "video": 100 * 1024 * 1024,  # 100MB
}

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    "image": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "audio": [".mp3", ".wav", ".ogg", ".m4a"],
    "video": [".mp4", ".avi", ".mov", ".mkv", ".webm"],
    "text": [".txt", ".md"]
}

# Languages supported
SUPPORTED_LANGUAGES = [
    "English", "Hindi", "Telugu", "Tamil", "Kannada", "Bengali", 
    "Marathi", "Gujarati", "Malayalam", "Punjabi", "Odia", "Assamese"
]

# Categories
CATEGORIES = [
    "Art", "Meme", "Culture", "Food", "Fables", "Events", "Music", "People",
    "Literature", "Architecture", "Skills", "Images", "Videos", "Flora", "Fauna",
    "Education", "Vegetation", "Folk Talks", "Traditional Skills", "Local History",
    "Local Locations", "Food & Agriculture", "Newspapers"
]

# Storage paths
DATA_DIR = Path("data")
UPLOADS_DIR = DATA_DIR / "uploads"
METADATA_DIR = DATA_DIR / "metadata"

# Create directories
DATA_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True)
METADATA_DIR.mkdir(exist_ok=True)

# Security settings
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
BCRYPT_ROUNDS = 12

# Firebase configuration (if using Firebase)
FIREBASE_CONFIG = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID")
}