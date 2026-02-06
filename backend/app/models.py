from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    original_name = Column(String)
    stored_name = Column(String)
    password_hash = Column(String)
    download_count = Column(Integer, default=0)
    max_downloads = Column(Integer, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer)
    ip_address = Column(String)
    timestamp = Column(DateTime, server_default=func.now())
