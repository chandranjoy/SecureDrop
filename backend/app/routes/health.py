from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from pathlib import Path

from app.database import engine
from app.config import UPLOAD_DIR

router = APIRouter()

@router.get("/health/ready")
def readiness_check():
    # ---- DB CHECK ----
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unready",
                "reason": "database_unavailable",
                "error": str(e)
            }
        )

    # ---- DISK CHECK ----
    try:
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        test_file = UPLOAD_DIR / ".healthcheck"
        test_file.write_text("ok")
        test_file.unlink()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unready",
                "reason": "upload_dir_unwritable",
                "error": str(e)
            }
        )

    return {
        "status": "ready",
        "database": "ok",
        "uploads": "ok"
    }
