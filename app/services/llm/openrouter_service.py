import os
import json

from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Always load .env from project root
ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(ROOT_DIR / ".env")

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError(
        f"OPENROUTER_API_KEY not found. Looking in: {ROOT_DIR / '.env'}"
    )

MODEL_NAME = os.getenv(
    "OPENROUTER_MODEL",
    "google/gemma-4-31b-it:free"
)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)


def generate_meeting_insights(transcript: str):

    prompt = f"""
You are a meeting analysis assistant.

Analyze the transcript and return ONLY valid JSON.

Format:

{{
    "summary": "string",
    "action_items": [
        {{
            "owner": "string or null",
            "task": "string"
        }}
    ],
    "decisions": [
        "decision 1"
    ],
    "follow_ups": [
        "follow up 1"
    ]
}}

Transcript:

{transcript}
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

    content = response.choices[0].message.content.strip()

    # Handle markdown-wrapped JSON
    if content.startswith("```"):
        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    return json.loads(content)