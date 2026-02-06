from fastapi import APIRouter, Request, Form
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from pathlib import Path

from app.database import SessionLocal
from app.models import File, AuditLog
from app.auth import verify_password
from app.config import UPLOAD_DIR

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# -------------------------------------------------
# PASSWORD PAGE
# -------------------------------------------------
@router.get("/download/{file_id}")
def download_page(request: Request, file_id: int):
    db: Session = SessionLocal()
    file = db.query(File).filter(File.id == file_id).first()
    db.close()

    if not file:
        return templates.TemplateResponse(
            "404.html",
            {"request": request, "message": "File not found"},
            status_code=404
        )

    return templates.TemplateResponse(
        "client_download.html",
        {"request": request, "file": file}
    )

# -------------------------------------------------
# VALIDATE PASSWORD
# -------------------------------------------------
@router.post("/download/{file_id}")
def validate_password(
    request: Request,
    file_id: int,
    password: str = Form(...)
):
    db: Session = SessionLocal()
    file = db.query(File).filter(File.id == file_id).first()

    if not file or not verify_password(password, file.password_hash):
        db.close()
        return templates.TemplateResponse(
            "client_download.html",
            {
                "request": request,
                "file": file,
                "error": "Invalid password"
            }
        )

    db.close()

    # Redirect to success page
    return RedirectResponse(
        url=f"/download/{file_id}/success",
        status_code=303
    )

# -------------------------------------------------
# SUCCESS PAGE (UI)
# -------------------------------------------------
@router.get("/download/{file_id}/success")
def download_success(request: Request, file_id: int):
    return templates.TemplateResponse(
        "download_success.html",
        {
            "request": request,
            "file_id": file_id
        }
    )

# -------------------------------------------------
# ACTUAL FILE DOWNLOAD
# -------------------------------------------------
@router.get("/download/{file_id}/file")
def download_file(request: Request, file_id: int):
    db: Session = SessionLocal()
    file = db.query(File).filter(File.id == file_id).first()

    if not file:
        db.close()
        return templates.TemplateResponse(
            "404.html",
            {"request": request, "message": "File not found"},
            status_code=404
        )

    # Expiry / limit checks
    if file.expires_at and datetime.utcnow() > file.expires_at:
        db.close()
        return templates.TemplateResponse(
            "404.html",
            {"request": request, "message": "Link expired"},
            status_code=404
        )

    if file.max_downloads and file.download_count >= file.max_downloads:
        db.close()
        return templates.TemplateResponse(
            "404.html",
            {"request": request, "message": "Download limit reached"},
            status_code=404
        )

    file_path: Path = UPLOAD_DIR / file.stored_name
    original_name = file.original_name

    if not file_path.exists():
        db.close()
        return templates.TemplateResponse(
            "404.html",
            {"request": request, "message": "File missing on server"},
            status_code=404
        )

    file.download_count += 1
    client_ip = request.client.host if request.client else "unknown"
    db.add(AuditLog(file_id=file.id, ip_address=client_ip))
    db.commit()
    db.close()

    return FileResponse(
        path=str(file_path),
        filename=original_name,
        media_type="application/octet-stream"
    )
