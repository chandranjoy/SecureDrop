from pathlib import Path
import uuid

from app.config import UPLOAD_DIR

def save_file(upload_file):
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    safe_name = f"{uuid.uuid4()}_{upload_file.filename}"
    file_path = UPLOAD_DIR / safe_name

    with open(file_path, "wb") as f:
        f.write(upload_file.file.read())

    return safe_name
