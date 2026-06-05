from app.services.llm.openrouter_service import (
    generate_meeting_insights
)

sample = """
John will prepare the deployment plan.

Sarah will review the API.

The team decided to use PostgreSQL.

Follow up meeting next Friday.
"""

result = generate_meeting_insights(
    sample
)

print(result)