from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from app.db.database import Base


class ChatFeedback(Base):

    __tablename__ = "chat_feedback"

    id = Column(
        Integer,
        primary_key=True
    )

    video_id = Column(
        Integer,
        ForeignKey("videos.id")
    )

    question = Column(String)

    answer = Column(String)

    rating = Column(String)