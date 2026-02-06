from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.init_admin import init_admin
from app.routes.admin_web import router as admin_router
from app.routes.client_web import router as client_router
from app.routes.health import router as health_router

Base.metadata.create_all(bind=engine)
init_admin()   # 🔐 SAFE, IDEMPOTENT

app = FastAPI(title="ZForto Secure Download Portal")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(health_router)
app.include_router(admin_router)
app.include_router(client_router)
