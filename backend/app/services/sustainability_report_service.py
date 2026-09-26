"""Campus sustainability report PDF generation backed by real analytics data."""

from __future__ import annotations

from datetime import date
from io import BytesIO
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.user import User
from app.services.campus_engine import get_campus_trend
from app.services.challenge_engine import list_challenges
from app.services.recommendation_engine import generate_recommendations


def _safe_round(value: float | int | None, digits: int = 2) -> float:
    try:
        return round(float(value or 0.0), digits)
    except (TypeError, ValueError):
        return 0.0


def _period_total_emission(db: Session, start_date: date, end_date: date) -> float:
    stmt = select(func.coalesce(func.sum(Activity.emission), 0.0)).where(
        Activity.activity_date >= start_date,
        Activity.activity_date <= end_date,
    )
    return _safe_round(db.scalar(stmt) or 0.0, 2)


def _period_active_users(db: Session, start_date: date, end_date: date) -> int:
    stmt = select(func.count(func.distinct(Activity.user_id))).where(
        Activity.activity_date >= start_date,
        Activity.activity_date <= end_date,
    )
    return int(db.scalar(stmt) or 0)


def _category_totals(db: Session, start_date: date, end_date: date) -> dict[str, float]:
    stmt = select(
        Activity.category,
        func.coalesce(func.sum(Activity.emission), 0.0).label("total_emission"),
    ).where(
        Activity.activity_date >= start_date,
        Activity.activity_date <= end_date,
    ).group_by(Activity.category)
    rows = db.execute(stmt).all()
    totals = {"travel": 0.0, "electricity": 0.0, "food": 0.0, "waste": 0.0}
    for category, total in rows:
        key = str(category).lower()
        if key in totals:
            totals[key] = _safe_round(total, 2)
    return totals


def _challenge_summary(db: Session) -> list[dict[str, Any]]:
    try:
        result = list_challenges(db=db)
        return result.get("challenges", [])[:3]
    except Exception:
        return []


def _recommendation_summary(db: Session, month: int, year: int) -> list[dict[str, Any]]:
    try:
        user = db.scalar(select(User.id).order_by(User.id.asc()))
        if user is None:
            return []
        result = generate_recommendations(user_id=int(user), month=month, year=year, db=db, limit=3)
        return result.get("recommendations", [])
    except Exception:
        return []


def generate_campus_sustainability_report_pdf(start_date: date, end_date: date, db: Session) -> bytes:
    """Generate a campus sustainability report PDF containing real, database-backed metrics."""
    if start_date > end_date:
        raise ValueError("start_date must be on or before end_date.")

    total_emission = _period_total_emission(db, start_date, end_date)
    active_users = _period_active_users(db, start_date, end_date)
    category_totals = _category_totals(db, start_date, end_date)
    trend = get_campus_trend(start_date=start_date, end_date=end_date, db=db).get("trend", [])

    month = start_date.month
    year = start_date.year
    pdf_buffer = BytesIO()
    story: list[Any] = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        spaceAfter=12,
        textColor=colors.HexColor("#1E3A5F"),
    )
    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=colors.HexColor("#1E3A5F"),
        spaceBefore=12,
        spaceAfter=8,
    )
    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
    )
    summary_style = ParagraphStyle(
        "SummaryStyle",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=10,
    )

    story.append(Paragraph("CarbonLens Sustainability Report", title_style))
    story.append(Paragraph(f"Reporting period: {start_date.isoformat()} to {end_date.isoformat()}", body_style))
    story.append(Spacer(1, 8 * mm))

    summary_rows = [
        [Paragraph("Total emissions", summary_style), f"{total_emission:,.2f} kgCO2e"],
        [Paragraph("Active users", summary_style), str(active_users)],
        [Paragraph("Average per active user", summary_style), f"{(total_emission / active_users):,.2f} kgCO2e" if active_users else "0.00 kgCO2e"],
        [Paragraph("Reporting month", summary_style), f"{year}-{month:02d}"],
    ]
    summary_table = Table(summary_rows, colWidths=[70 * mm, 70 * mm])
    summary_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCEAF7")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
        ])
    )
    story.append(summary_table)
    story.append(Spacer(1, 8 * mm))

    story.append(Paragraph("Executive Summary", heading_style))
    story.append(
        Paragraph(
            "This report summarizes the campus emissions footprint for the requested reporting period using the existing CarbonLens activity and analytics data. "
            "All values are calculated from stored activity records and existing emission-factor logic rather than sample estimates.",
            body_style,
        )
    )
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph("Emissions breakdown by category", heading_style))
    breakdown_rows = [["Category", "kgCO2e", "%"]]
    total = sum(category_totals.values())
    for category in ["travel", "electricity", "food", "waste"]:
        value = category_totals.get(category, 0.0)
        percentage = (value / total * 100.0) if total > 0 else 0.0
        breakdown_rows.append([category.title(), f"{value:,.2f}", f"{percentage:.1f}%"])
    breakdown_table = Table(breakdown_rows, colWidths=[50 * mm, 45 * mm, 25 * mm])
    breakdown_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E7F0FA")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ])
    )
    story.append(breakdown_table)
    story.append(Spacer(1, 8 * mm))

    story.append(Paragraph("Monthly trend", heading_style))
    trend_rows = [["Month", "Emission (kgCO2e)"]]
    for item in trend[:12]:
        trend_rows.append([str(item.get("month", "n/a")), f"{_safe_round(item.get('emission'), 2):,.2f}"])
    if not trend:
        trend_rows.append([start_date.strftime("%Y-%m"), "0.00"])
    trend_table = Table(trend_rows, colWidths=[50 * mm, 50 * mm])
    trend_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E7F0FA")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ])
    )
    story.append(trend_table)
    story.append(Spacer(1, 8 * mm))

    recommendations = _recommendation_summary(db, month, year)
    story.append(Paragraph("Priority recommendations", heading_style))
    if recommendations:
        for recommendation in recommendations:
            title = recommendation.get("title", "Opportunity")
            saving = _safe_round(recommendation.get("potential_saving", 0.0))
            story.append(Paragraph(f"- {title} (potential saving: {saving:,.2f} kgCO2e)", body_style))
    else:
        story.append(Paragraph("No recommendations were available for the selected period.", body_style))
    story.append(Spacer(1, 5 * mm))

    challenges = _challenge_summary(db)
    story.append(Paragraph("Challenge highlights", heading_style))
    if challenges:
        for challenge in challenges:
            name = challenge.get("name", "Challenge")
            status = challenge.get("status", "active")
            story.append(Paragraph(f"- {name} ({status})", body_style))
    else:
        story.append(Paragraph("No active challenge data was available for this reporting window.", body_style))
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph("Methodology", heading_style))
    story.append(
        Paragraph(
            "Metrics in this report are derived from the CarbonLens database using activity records, emissions already calculated by the application, and the configured emission factors. "
            "Trends are grouped by month and category to maintain a consistent campus view across the selected date range.",
            body_style,
        )
    )

    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
    )
    doc.build(story)
    return pdf_buffer.getvalue()
