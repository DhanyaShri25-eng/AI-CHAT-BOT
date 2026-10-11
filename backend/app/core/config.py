from typing import List
from pydantic import BaseModel, Field
import os

class Settings(BaseModel):
    PROJECT_NAME: str = "BuildWise AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Environment & Host
    ENV: str = os.getenv("ENV", "development")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "buildwise-ai-super-secret-key-makeathon-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database (Defaults to local SQLite async for out-of-the-box zero-config execution; accepts PostgreSQL/Supabase URI)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./buildwise.db")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*"
    ]
    
    # AI / LLM Configuration
    # Options: "built-in" (intelligent engineering agent), "ollama", "openai-compatible", "gemini", "groq", "huggingface"
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "built-in")
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "buildwise-llama3-construction-8b")
    LLM_API_BASE_URL: str = os.getenv("LLM_API_BASE_URL", "http://localhost:11434/v1")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 4096
    
    # Voice / Whisper
    WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "base")
    TTS_DEFAULT_VOICE: str = "ta-IN-ValluvarNeural"
    
    # Storage
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")

settings = Settings()
