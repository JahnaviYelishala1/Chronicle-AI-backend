import os

from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

from app.services.rag.search_service import (
    search_chunks
)

from app.services.llm.verification_service import (
    verify_answer
)

ROOT_DIR = Path(__file__).resolve().parents[3]

load_dotenv(
    ROOT_DIR / ".env"
)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv(
        "OPENROUTER_API_KEY"
    )
)

MODEL_NAME = os.getenv(
    "OPENROUTER_MODEL",
    "google/gemma-4-31b-it:free"
)


def answer_question(
    video_id: int,
    question: str
):

    chunks = search_chunks(
        video_id=video_id,
        query=question,
        limit=5
    )

    if not chunks:

        return {
            "answer": "No information found.",
            "retrieval_confidence": 0,
            "verified": False,
            "verification_confidence": 0,
            "reason": "No supporting context found.",
            "sources": []
        }

    top_similarity = chunks[0]["similarity"]

    retrieval_confidence = round(
        max(
            0,
            min(
                100,
                top_similarity * 100
            )
        ),
        2
    )

    context = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )

    prompt = f"""
You are a meeting assistant.

Answer ONLY using the provided context.

If the answer cannot be found in the context,
reply exactly:

I could not find that information.

Context:

{context}

Question:

{question}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    answer = (
        response
        .choices[0]
        .message
        .content
    )

    verification = verify_answer(
        question=question,
        answer=answer,
        context=context
    )

    return {

        "answer": answer,

        "retrieval_confidence":
        retrieval_confidence,

        "verified":
        verification.get(
            "verified",
            False
        ),

        "verification_confidence":
        verification.get(
            "confidence",
            0
        ),

        "reason":
        verification.get(
            "reason",
            ""
        ),

        "sources": [
            {
                "chunk_id":
                chunk["chunk_id"],

                "similarity":
                round(
                    chunk["similarity"] * 100,
                    2
                ),

                "text":
                chunk["text"][:200]
            }
            for chunk in chunks
        ]
    }