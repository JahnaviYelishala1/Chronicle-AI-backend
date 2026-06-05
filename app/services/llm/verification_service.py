import json

from app.services.llm.openrouter_service import (
    client,
    MODEL_NAME
)


def verify_answer(
    question: str,
    answer: str,
    context: str
):

    prompt = f"""
You are an answer verification system.

Question:
{question}

Answer:
{answer}

Context:
{context}

Determine whether the answer is fully supported by the context.

Return ONLY valid JSON:

{{
    "verified": true,
    "confidence": 95,
    "reason": "Answer is directly supported by the context."
}}
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

    content = response.choices[0].message.content

    if content.startswith("```"):
        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    return json.loads(content)