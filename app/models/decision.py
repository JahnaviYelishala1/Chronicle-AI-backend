from sqlalchemy import Column, Integer, Text, ForeignKey

from app.db.database import Base


class Decision(Base):
    __tablename__ = "decisions"

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

    decision = Column(
        Text,
        nullable=False
    )