from fastapi import APIRouter, Request, Form, UploadFile, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Admin, AuditLog, File
from app.auth import verify_password, hash_password
from app.utils.storage import save_file
from app.deps import require_admin
from app.config import UPLOAD_DIR
#from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---- LOGIN PAGE ----
@router.get("/admin/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/admin/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    admin = db.query(Admin).filter(Admin.username == username).first()

    if not admin or not verify_password(password, admin.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid credentials"}
        )

    response = RedirectResponse("/admin/dashboard", status_code=302)

    response.set_cookie(
        key="admin",
        value=admin.username,
        httponly=True,
        secure=False,     # set True when HTTPS is enabled
        samesite="lax"
    )

    return response

# ---- DASHBOARD ----
@router.get("/admin/dashboard")
def dashboard(
    request: Request,
    admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    files = db.query(File).all()
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "files": files, "admin": admin}
    )

# ---- UPLOAD ----
@router.post("/admin/upload")
def upload_file(
    request: Request,
    file: UploadFile,
    file_password: str = Form(...),
    admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    stored_name = save_file(file)
    new_file = File(
        original_name=file.filename,
        stored_name=stored_name,
        password_hash=hash_password(file_password)
    )
    db.add(new_file)
    db.commit()
    return RedirectResponse("/admin/dashboard", status_code=302)

# ---- DELETE ----
@router.post("/admin/delete/{file_id}")
def delete_file(
    file_id: int,
    admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        return RedirectResponse("/admin/dashboard", status_code=302)

    file_path = UPLOAD_DIR / file.stored_name
    if file_path.exists():
        file_path.unlink()  # delete file from disk

    db.delete(file)
    db.commit()

    return RedirectResponse("/admin/dashboard", status_code=302)

# ---- REPLACE ----
@router.post("/admin/replace/{file_id}")
def replace_file(
    file_id: int,
    file: UploadFile,
    admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    existing = db.query(File).filter(File.id == file_id).first()
    if not existing:
        return RedirectResponse("/admin/dashboard", status_code=302)

    # delete old file
    old_path = UPLOAD_DIR / existing.stored_name
    if old_path.exists():
        old_path.unlink()

    # save new file
    new_stored = save_file(file)
    existing.stored_name = new_stored
    existing.original_name = file.filename
    existing.download_count = 0

    db.commit()
    return RedirectResponse("/admin/dashboard", status_code=302)

# ---- AUDIT LOG ----
@router.get("/admin/audit")
def audit_logs(
    request: Request,
    admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    logs = (
        db.query(AuditLog, File)
        .join(File, AuditLog.file_id == File.id)
        .order_by(AuditLog.timestamp.desc())
        .limit(500)
        .all()
    )

    return templates.TemplateResponse(
        "audit.html",
        {
            "request": request,
            "admin": admin,
            "logs": logs
        }
    )

# ---- LOGOUT ----
@router.get("/admin/logout")
def logout():
    response = RedirectResponse("/admin/login", status_code=302)
    response.delete_cookie("admin")
    return response
