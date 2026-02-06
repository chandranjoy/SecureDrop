from pathlib import Path

# ---- BASE PATHS ----
BASE_DIR = Path("/opt/securedrop/backend")

UPLOAD_DIR = BASE_DIR / "uploads"
DATA_DIR = BASE_DIR / "data"

DATABASE_URL = "sqlite:////opt/securedrop/backend/data/data.db"

# ---- SECURITY (AUTH) ----
SECRET_KEY = "YOUR_PASSWORD"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
