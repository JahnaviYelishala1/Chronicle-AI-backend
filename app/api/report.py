from fastapi import APIRouter
from fastapi.responses import Response

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

from app.services.pdf.pdf_service import (
    generate_pdf_report
)

router = APIRouter()


@router.get("/report/{video_id}")
def download_report(video_id: int):

    db = SessionLocal()

    try:

        video = (
            db.query(Video)
            .filter(Video.id == video_id)
            .first()
        )

        transcript = (
            db.query(Transcript)
            .filter(
                Transcript.video_id == video_id
            )
            .first()
        )

        insight = (
            db.query(MeetingInsight)
            .filter(
                MeetingInsight.video_id == video_id
            )
            .first()
        )

        action_items = (
            db.query(ActionItem)
            .filter(
                ActionItem.insight_id ==
                insight.id
            )
            .all()
        )

        decisions = (
            db.query(Decision)
            .filter(
                Decision.insight_id ==
                insight.id
            )
            .all()
        )

        follow_ups = (
            db.query(FollowUp)
            .filter(
                FollowUp.insight_id ==
                insight.id
            )
            .all()
        )

        pdf = generate_pdf_report(
            title=video.title,
            summary=insight.summary,
            action_items=[
                f"{item.owner}: {item.task}"
                for item in action_items
            ],
            decisions=[
                d.decision
                for d in decisions
            ],
            follow_ups=[
                f.follow_up
                for f in follow_ups
            ],
            transcript=transcript.content
        )

        return Response(
            content=pdf,
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                f"attachment; filename=meeting_{video_id}.pdf"
            }
        )

    finally:

        db.close()