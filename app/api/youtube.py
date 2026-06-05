from fastapi import APIRouter
from uuid import uuid4
import os

from app.schemas.youtube import YoutubeRequest

from app.services.youtube.youtube_downloader import (
    download_youtube_audio
)

from app.core.supabase import supabase

from app.db.database import SessionLocal
from app.models.video import Video


router = APIRouter()

BUCKET_NAME = os.getenv(
    "SUPABASE_BUCKET"
)


@router.post("/youtube")
def upload_youtube_video(
    request: YoutubeRequest
):

    local_file, title = (
        download_youtube_audio(
            request.url
        )
    )

    file_extension = (
        os.path.splitext(local_file)[1]
    )

    unique_filename = (
        f"{uuid4()}{file_extension}"
    )

    print("LOCAL FILE:", local_file)
    print("EXISTS:", os.path.exists(local_file))

    with open(
        local_file,
        "rb"
    ) as f:

        file_bytes = f.read()

    supabase.storage.from_(
        BUCKET_NAME
    ).upload(
        path=unique_filename,
        file=file_bytes,
        file_options={
            "content-type": "audio/mpeg"
        }
    )

    file_url = (
        supabase.storage
        .from_(BUCKET_NAME)
        .get_public_url(
            unique_filename
        )
    )

    db = SessionLocal()

    try:

        new_video = Video(
            title=title,
            source_type="youtube",
            file_path=file_url,
            storage_path=unique_filename
        )

        db.add(new_video)
        db.commit()
        db.refresh(new_video)

        return {
            "id": new_video.id,
            "title": title,
            "file_url": file_url
        }

    finally:

        db.close()

        if os.path.exists(
            local_file
        ):
            os.remove(local_file)