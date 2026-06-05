from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def generate_pdf_report(
    title,
    summary,
    action_items,
    decisions,
    follow_ups,
    transcript
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Chronicle AI Meeting Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            f"Meeting: {title}",
            styles["Heading2"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            "Summary",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            summary or "N/A",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            "Action Items",
            styles["Heading2"]
        )
    )

    for item in action_items:
        content.append(
            Paragraph(
                item,
                styles["Normal"]
            )
        )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            "Decisions",
            styles["Heading2"]
        )
    )

    for decision in decisions:
        content.append(
            Paragraph(
                decision,
                styles["Normal"]
            )
        )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            "Follow Ups",
            styles["Heading2"]
        )
    )

    for follow_up in follow_ups:
        content.append(
            Paragraph(
                follow_up,
                styles["Normal"]
            )
        )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            "Transcript",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            transcript[:5000],
            styles["Normal"]
        )
    )

    doc.build(content)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf