from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import File, AuditLog
from app.auth import verify_password
import os

router = APIRouter()
