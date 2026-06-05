from fastapi import APIRouter

from app.db.database import SessionLocal

from app.models.chat_feedback import (
    ChatFeedback
)

router = APIRouter()


@router.post("/feedback")
def save_feedback(
    payload: dict
):

    db = SessionLocal()

    try:

        feedback = ChatFeedback(
            video_id=payload["video_id"],
            question=payload["question"],
            answer=payload["answer"],
            rating=payload["rating"]
        )

        db.add(feedback)

        db.commit()

        return {
            "message": "Feedback saved"
        }

    finally:

        db.close()