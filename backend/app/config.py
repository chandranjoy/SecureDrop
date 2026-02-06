from pathlib import Path

# ---- BASE PATHS ----
BASE_DIR = Path("/opt/secure-file-share/backend")

UPLOAD_DIR = BASE_DIR / "uploads"
DATA_DIR = BASE_DIR / "data"

DATABASE_URL = "sqlite:////opt/secure-file-share/backend/data/data.db"

# ---- SECURITY (AUTH) ----
SECRET_KEY = "Zf0rt0_2O26^"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
