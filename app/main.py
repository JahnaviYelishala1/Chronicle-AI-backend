import os
import sys
from pathlib import Path
from loguru import logger

# Load .env file first (before any other imports)
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

from fastapi import FastAPI

from app.api.video import router as video_router
from app.api.upload import router as upload_router
from app.api.transcription import router as transcription_router
from app.api.chat import (
    router as chat_router
)
from app.api.youtube import (
    router as youtube_router
)
from app.api.videos import (
    router as videos_router
)
from app.api.feedback import (
    router as feedback_router
)
from app.api.report import (
    router as report_router
)
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
log_level = os.getenv("LOG_LEVEL", "info").upper()
logger.remove()
logger.add(
    sys.stdout,
    level=log_level,
    format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

logger.info("Starting Chronicle AI Backend...")

app = FastAPI(title="Chronicle AI")

cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173"
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(video_router)
app.include_router(upload_router)
app.include_router(transcription_router)
app.include_router(chat_router)
app.include_router(youtube_router)
app.include_router(videos_router)
app.include_router(
    feedback_router
)
app.include_router(
    report_router
)

@app.on_event("startup")
async def startup_event():
    """Validate environment variables and dependencies on startup"""
    logger.info("🚀 Running startup validation...")
    
    required_vars = [
        "DATABASE_URL",
        "SUPABASE_URL",
        "SUPABASE_SERVICE_KEY",
        "OPENROUTER_API_KEY",
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            logger.warning(f"⚠️  Missing environment variable: {var}")
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please set these variables before deploying")
    else:
        logger.info("✓ All required environment variables present")
    
    logger.info("✓ Startup validation complete")


@app.get("/")
def root():
    return {
        "message": "Chronicle AI Running",
        "status": "healthy"
    }


@app.get("/health")
def health_check():
    """Simple health check endpoint"""
    return {
        "status": "ok",
        "service": "chronicle-ai-backend"
    }


@app.get("/health/detailed")
def detailed_health():
    """Detailed health check with environment info"""
    return {
        "status": "ok",
        "service": "chronicle-ai-backend",
        "environment": {
            "database_configured": bool(os.getenv("DATABASE_URL")),
            "supabase_configured": bool(os.getenv("SUPABASE_URL")),
            "openrouter_configured": bool(os.getenv("OPENROUTER_API_KEY")),
            "cors_origins": os.getenv("CORS_ORIGINS", "not set"),
        }
    }
