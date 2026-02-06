from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import File
from app.auth import hash_password
from app.utils.storage import save_file

router = APIRouter(prefix="/admin")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/upload")
def upload(
    file: UploadFile,
    file_password: str,
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
    return {"file_id": new_file.id}
