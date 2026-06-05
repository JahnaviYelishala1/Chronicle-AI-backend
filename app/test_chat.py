from app.services.rag.chat_service import (
    answer_question
)

result = answer_question(
    video_id=5,
    question="What adjectives were discussed?"
)

print(result)