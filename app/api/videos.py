from fastapi import APIRouter, HTTPException

from app.db.database import SessionLocal

from app.models.video import Video
from app.models.transcript import Transcript

from app.models.meeting_insight import (
    MeetingInsight
)

from app.models.action_item import (
    ActionItem
)

from app.models.decision import (
    Decision
)

from app.models.follow_up import (
    FollowUp
)

router = APIRouter()


@router.get("/videos")
def get_videos():

    db = SessionLocal()

    try:

        videos = (
            db.query(Video)
            .order_by(Video.id.desc())
            .all()
        )

        return [
            {
                "id": video.id,
                "title": video.title,
                "status": video.status,
                "source_type": video.source_type,
                "created_at": video.created_at
            }
            for video in videos
        ]

    finally:
        db.close()


@router.get("/video/{video_id}")
def get_video(video_id: int):

    db = SessionLocal()

    try:

        video = (
            db.query(Video)
            .filter(Video.id == video_id)
            .first()
        )

        if not video:
            raise HTTPException(
                status_code=404,
                detail="Video not found"
            )

        return {
            "id": video.id,
            "title": video.title,
            "status": video.status,
            "source_type": video.source_type,
            "created_at": video.created_at
        }

    finally:
        db.close()


@router.get("/insights/{video_id}")
def get_insights(video_id: int):

    db = SessionLocal()

    try:

        insight = (
            db.query(MeetingInsight)
            .filter(
                MeetingInsight.video_id == video_id
            )
            .first()
        )

        if not insight:
            raise HTTPException(
                status_code=404,
                detail="Insights not found"
            )

        action_items = (
            db.query(ActionItem)
            .filter(
                ActionItem.insight_id == insight.id
            )
            .all()
        )

        decisions = (
            db.query(Decision)
            .filter(
                Decision.insight_id == insight.id
            )
            .all()
        )

        follow_ups = (
            db.query(FollowUp)
            .filter(
                FollowUp.insight_id == insight.id
            )
            .all()
        )

        return {
            "summary": insight.summary,

            "action_items": [
                {
                    "owner": item.owner,
                    "task": item.task
                }
                for item in action_items
            ],

            "decisions": [
                decision.decision
                for decision in decisions
            ],

            "follow_ups": [
                follow_up.follow_up
                for follow_up in follow_ups
            ]
        }

    finally:
        db.close()


@router.get("/transcript/{video_id}")
def get_transcript(video_id: int):

    db = SessionLocal()

    try:

        transcript = (
            db.query(Transcript)
            .filter(
                Transcript.video_id == video_id
            )
            .first()
        )

        if not transcript:
            raise HTTPException(
                status_code=404,
                detail="Transcript not found"
            )

        return {
            "content": transcript.content
        }

    finally:
        db.close()