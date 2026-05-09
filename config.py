import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

USERS_URL = os.getenv("USERS_URL", "https://jsonplaceholder.typicode.com/users")
POSTS_URL = os.getenv("POSTS_URL", "https://jsonplaceholder.typicode.com/posts")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "processed_users.csv")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
USE_LOCAL_FALLBACK = os.getenv("USE_LOCAL_FALLBACK", "true").lower() == "true"
DATABASE_URL = os.getenv("DATABASE_URL", "")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://127.0.0.1:5678/webhook/csv-ready")

