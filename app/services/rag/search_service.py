from sqlalchemy import text

from app.db.database import SessionLocal

from app.services.embeddings.embedding_service import (
    generate_embedding
)


def search_chunks(
    video_id: int,
    query: str,
    limit: int = 5
):

    db = SessionLocal()

    try:

        query_embedding = generate_embedding(
            query
        )

        sql = text("""
    SELECT
        tc.id,
        tc.chunk_text,
        (
            1 - (
                e.embedding <=> CAST(:embedding AS vector)
            )
        ) AS similarity

    FROM embeddings e

    JOIN transcript_chunks tc
        ON tc.id = e.chunk_id

    JOIN transcripts t
        ON t.id = tc.transcript_id

    WHERE t.video_id = :video_id

    ORDER BY
        e.embedding <=> CAST(:embedding AS vector)

    LIMIT :limit
""")

        result = db.execute(
            sql,
            {
                "video_id": video_id,
                "embedding": str(query_embedding),
                "limit": limit
            }
        )

        return [
    {
        "chunk_id": row.id,
        "text": row.chunk_text,
        "similarity": float(row.similarity)
    }
    for row in result
]

    finally:
        db.close()