from sqlalchemy import Column, Integer, Text, ForeignKey

from app.db.database import Base


class MeetingInsight(Base):
    __tablename__ = "meeting_insights"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    video_id = Column(
        Integer,
        ForeignKey("videos.id"),
        nullable=False
    )

    summary = Column(
        Text,
        nullable=False
    )