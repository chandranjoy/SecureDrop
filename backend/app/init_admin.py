import os
from dotenv import load_dotenv

from app.database import SessionLocal
from app.models import Admin
from app.auth import hash_password

load_dotenv("/opt/securedrop/backend/.env")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

def init_admin():
    if not ADMIN_USERNAME or not ADMIN_PASSWORD:
        return  # silently skip if not configured

    db = SessionLocal()

    exists = db.query(Admin).filter(
        Admin.username == ADMIN_USERNAME
    ).first()

    if exists:
        db.close()
        return  # admin already exists → do nothing

    admin = Admin(
        username=ADMIN_USERNAME,
        password_hash=hash_password(ADMIN_PASSWORD)
    )

    db.add(admin)
    db.commit()
    db.close()
