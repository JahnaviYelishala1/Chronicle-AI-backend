from fastapi import APIRouter, HTTPException
import os

from app.db.database import SessionLocal
from app.models.video import Video
from app.models.transcript import Transcript

from app.services.transcription.whisper_service import (
    transcribe_audio
)

from app.services.transcription.supabase_downloader import (
    download_from_supabase
)
from app.models.transcript_chunk import TranscriptChunk

from app.services.chunking.text_chunker import (
    chunk_text
)
from app.models.embedding import Embedding

from app.services.embeddings.embedding_service import (
    generate_embedding
)
from app.services.llm.openrouter_service import (
    generate_meeting_insights
)

from app.models.meeting_insight import (
    MeetingInsight
)

from app.models.action_item import (
    ActionItem
)

from app.models.decision import (
    Decision
)

from app.models.follow_up import (
    FollowUp
)

router = APIRouter()

BUCKET_NAME = os.getenv("SUPABASE_BUCKET")


@router.post("/transcribe/{video_id}")
def transcribe(video_id: int):

    db = SessionLocal()

    try:

        video = (
            db.query(Video)
            .filter(Video.id == video_id)
            .first()
        )

        if not video:
            raise HTTPException(
                status_code=404,
                detail="Video not found"
            )

        if not video.storage_path:
            raise HTTPException(
                status_code=400,
                detail="storage_path missing"
            )
        
        video.status = "processing"
        db.commit()

        local_file = download_from_supabase(
            BUCKET_NAME,
            video.storage_path
        )

        transcript_text = transcribe_audio(
            local_file
        )

        transcript = Transcript(
            video_id=video.id,
            content=transcript_text
        )

        db.add(transcript)
        db.commit()
        db.refresh(transcript)

        insights = generate_meeting_insights(
    transcript_text
)

        meeting_insight = MeetingInsight(
    video_id=video.id,
    summary=insights["summary"]
)
        db.add(meeting_insight)
        db.commit()
        db.refresh(meeting_insight)

        for item in insights["action_items"]:
             db.add(
                  ActionItem(
            insight_id=meeting_insight.id,
            owner=item.get("owner"),
            task=item["task"]
        )
    )
             db.commit()
        
        for decision in insights["decisions"]:
            db.add(
        Decision(
            insight_id=meeting_insight.id,
            decision=decision
        )
    )
            db.commit()

        for follow_up in insights["follow_ups"]:
             db.add(
        FollowUp(
            insight_id=meeting_insight.id,
            follow_up=follow_up
        )
    )
             db.commit()

        chunks = chunk_text(transcript_text)

        for chunk in chunks:

            chunk_record = TranscriptChunk(
            transcript_id=transcript.id,
            chunk_text=chunk
            )

            db.add(chunk_record)
            db.commit()
            db.refresh(chunk_record)
            vector = generate_embedding(chunk)
            embedding_record = Embedding(
        chunk_id=chunk_record.id,
        embedding=vector
    )
            db.add(embedding_record)
            db.commit()


        video.status = "completed"
        db.commit()
        return {
    "message": "Transcript processed",
    "characters": len(transcript_text),
    "chunks_created": len(chunks),
    "summary_created": True,
    "action_items": len(insights["action_items"]),
    "decisions": len(insights["decisions"]),
    "follow_ups": len(insights["follow_ups"])
}

    finally:
        db.close()

