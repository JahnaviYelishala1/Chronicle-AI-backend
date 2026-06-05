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

app = FastAPI(title="Chronicle AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
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

@app.get("/")
def root():
    return {
        "message": "Chronicle AI Running"
    }