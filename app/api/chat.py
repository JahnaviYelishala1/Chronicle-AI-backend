from fastapi import APIRouter

from app.schemas.chat import ChatRequest

from app.services.rag.chat_service import (
    answer_question
)

router = APIRouter()


@router.post("/chat/{video_id}")
def chat(
    video_id: int,
    request: ChatRequest
):

    return answer_question(
        video_id=video_id,
        question=request.question
    )