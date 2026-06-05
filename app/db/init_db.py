from app.db.database import engine, Base
from app.models.video import Video
from app.models.transcript import Transcript
from app.models.transcript_chunk import TranscriptChunk
from app.models.embedding import Embedding
from app.models.meeting_insight import MeetingInsight
from app.models.action_item import ActionItem
from app.models.decision import Decision
from app.models.follow_up import FollowUp
from app.models.chat_feedback import (
    ChatFeedback
)
Base.metadata.create_all(bind=engine)

print("Tables created successfully!")