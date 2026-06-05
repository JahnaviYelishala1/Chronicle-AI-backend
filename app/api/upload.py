from fastapi import APIRouter, UploadFile, File
from uuid import uuid4
import os

from app.core.supabase import supabase
from app.db.database import SessionLocal
from app.models.video import Video

router = APIRouter()

BUCKET_NAME = os.getenv("SUPABASE_BUCKET")


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4()}{file_extension}"

    file_bytes = await file.read()

    supabase.storage.from_(BUCKET_NAME).upload(
        path=unique_filename,
        file=file_bytes,
        file_options={
            "content-type": file.content_type
        }
    )

    file_url = supabase.storage.from_(BUCKET_NAME).get_public_url(
        unique_filename
    )

    db = SessionLocal()

    try:
        new_video = Video(
    title=file.filename,
    source_type="upload",
    file_path=file_url,
    storage_path=unique_filename
)

        db.add(new_video)
        db.commit()
        db.refresh(new_video)

        return {
            "id": new_video.id,
            "file_url": file_url
        }

    finally:
        db.close()