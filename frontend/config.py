import os
from dotenv import load_dotenv

load_dotenv()

# API base url
API_BASE_URL_BACKEND = os.getenv("API_BASE_URL_BACKEND")
API_BASE_URL_CONTAINER = os.getenv("API_BASE_URL_CONTAINER")

# OAuth2 Credentials
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
