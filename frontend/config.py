import os
from dotenv import load_dotenv

load_dotenv()

# API base url
API_BASE_URL_BACKEND_USER = os.getenv("API_BASE_URL_BACKEND_USER")
API_BASE_URL_BACKEND_SERVICE = os.getenv("API_BASE_URL_BACKEND_SERVICE")

# OAuth2 Credentials
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
