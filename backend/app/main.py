from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
import os

from backend.app.core.config import settings
from backend.app.core.database import init_db
from backend.app.api.auth import router as auth_router
from backend.app.api.chat import router as chat_router
from backend.app.api.voice import router as voice_router
from backend.app.api.projects import router as projects_router
from backend.app.api.designs import router as designs_router
from backend.app.api.estimates import router as estimates_router
from backend.app.api.materials import router as materials_router
from backend.app.api.schedules import router as schedules_router
from backend.app.api.documents import router as documents_router
from backend.app.api.system import router as system_router
from backend.app.api.training import router as training_router
from backend.app.api.pictures import router as pictures_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure upload dir and initialize database tables
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    await init_db()
    print("[INFO] BuildWise AI Database initialized successfully.")
    yield
    print("[INFO] BuildWise AI Backend shutdown.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Full-Stack AI-Powered Building Design, Architecture, Construction Cost Estimation & Scheduling Platform",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time, 4))
    return response

# Mount API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(chat_router, prefix=settings.API_V1_STR)
app.include_router(voice_router, prefix=settings.API_V1_STR)
app.include_router(projects_router, prefix=settings.API_V1_STR)
app.include_router(designs_router, prefix=settings.API_V1_STR)
app.include_router(estimates_router, prefix=settings.API_V1_STR)
app.include_router(materials_router, prefix=settings.API_V1_STR)
app.include_router(schedules_router, prefix=settings.API_V1_STR)
app.include_router(documents_router, prefix=settings.API_V1_STR)
app.include_router(system_router, prefix=settings.API_V1_STR)
app.include_router(training_router, prefix=settings.API_V1_STR)
app.include_router(pictures_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs",
        "health_check": f"{settings.API_V1_STR}/health"
    }
