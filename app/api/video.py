from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.video import Video
from app.schemas.video import VideoCreate

router = APIRouter()


@router.post("/videos")
def create_video(video: VideoCreate):

    db: Session = SessionLocal()

    try:
        new_video = Video(
            title=video.title,
            source_type=video.source_type,
            file_path=video.file_path
        )

        db.add(new_video)
        db.commit()
        db.refresh(new_video)

        return {
            "id": new_video.id,
            "title": new_video.title
        }

    finally:
        db.close()