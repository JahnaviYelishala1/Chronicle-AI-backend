from sqlalchemy import Column, Integer, Text, ForeignKey

from app.db.database import Base


class ActionItem(Base):
    __tablename__ = "action_items"

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

    owner = Column(
        Text,
        nullable=True
    )

    task = Column(
        Text,
        nullable=False
    )