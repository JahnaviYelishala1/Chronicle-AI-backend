from sqlalchemy import Column, Integer, ForeignKey
from pgvector.sqlalchemy import Vector

from app.db.database import Base


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    chunk_id = Column(
        Integer,
        ForeignKey("transcript_chunks.id"),
        nullable=False
    )

    embedding = Column(
        Vector(384)
    )