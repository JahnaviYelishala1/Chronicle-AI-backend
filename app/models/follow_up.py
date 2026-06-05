from sqlalchemy import Column, Integer, Text, ForeignKey

from app.db.database import Base


class FollowUp(Base):
    __tablename__ = "follow_ups"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    insight_id = Column(
        Integer,
        ForeignKey("meeting_insights.id"),
        nullable=False
    )

    follow_up = Column(
        Text,
        nullable=False
    )