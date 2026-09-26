"""Campus-wide Carbon Analytics Engine & Aggregation Service.

Handles SQL aggregation for campus overview, monthly trends, department analytics,
hostel analytics, user benchmark against campus averages, and leaderboard data.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.department import Department
from app.models.hostel import Hostel
from app.models.user import User
from app.services.exceptions import UserNotFoundError


def get_campus_overview(
    month: int | None,
    year: int | None,
    db: Session,
) -> dict[str, Any]:
    """Calculate campus-wide total emissions, active user count, average per active user, and category breakdown."""
    # Base filter for month/year if supplied
    act_filters = []
    if year is not None:
        act_filters.append(extract("year", Activity.activity_date) == year)
    if month is not None:
        act_filters.append(extract("month", Activity.activity_date) == month)

    # 1. Total campus emission
    stmt_tot = select(func.coalesce(func.sum(Activity.emission), 0.0))
    if act_filters:
        stmt_tot = stmt_tot.where(*act_filters)
    total_emission = float(db.scalar(stmt_tot) or 0.0)

    # 2. Active users count
    stmt_active = select(func.count(func.distinct(Activity.user_id)))
    if act_filters:
        stmt_active = stmt_active.where(*act_filters)
    active_users = int(db.scalar(stmt_active) or 0)

    # 3. Average per active user
    avg_per_active_user = (total_emission / active_users) if active_users > 0 else 0.0

    # 4. Category breakdown
    stmt_cat = select(
        Activity.category,
        func.coalesce(func.sum(Activity.emission), 0.0).label("cat_emission"),
    )
    if act_filters:
        stmt_cat = stmt_cat.where(*act_filters)
    stmt_cat = stmt_cat.group_by(Activity.category)

    rows = db.execute(stmt_cat).all()
    cat_emissions = {r.category.lower(): float(r.cat_emission) for r in rows}

    categories_result = {}
    percentages_result = {}
    for cat in ["travel", "electricity", "food", "waste"]:
        val = cat_emissions.get(cat, 0.0)
        categories_result[cat] = round(val, 4)
        pct = (val / total_emission * 100.0) if total_emission > 0 else 0.0
        percentages_result[cat] = round(pct, 2)

    return {
        "month": month,
        "year": year,
        "total_emission": round(total_emission, 4),
        "active_users": active_users,
        "average_per_active_user": round(avg_per_active_user, 4),
        "unit": "kgCO2e",
        "categories": categories_result,
        "category_percentages": percentages_result,
    }


def get_campus_trend(
    start_date: date | None,
    end_date: date | None,
    db: Session,
) -> dict[str, Any]:
    """Retrieve campus-wide monthly emission totals in chronological order."""
    stmt = select(
        extract("year", Activity.activity_date).label("yr"),
        extract("month", Activity.activity_date).label("mo"),
        func.coalesce(func.sum(Activity.emission), 0.0).label("tot"),
    )

    if start_date:
        stmt = stmt.where(Activity.activity_date >= start_date)
    if end_date:
        stmt = stmt.where(Activity.activity_date <= end_date)

    stmt = stmt.group_by("yr", "mo").order_by("yr", "mo")

    rows = db.execute(stmt).all()
    trend_items = []
    for yr, mo, tot in rows:
        month_str = f"{int(yr):04d}-{int(mo):02d}"
        trend_items.append({"month": month_str, "emission": round(float(tot), 4)})

    return {"trend": trend_items}


def get_department_analytics(
    month: int | None,
    year: int | None,
    db: Session,
) -> dict[str, Any]:
    """Retrieve population, active user count, total emissions, average per user, and category breakdown per department."""
    departments = db.scalars(select(Department).order_by(Department.name)).all()

    dept_results = []
    for dept in departments:
        # Total registered users
        total_users = int(
            db.scalar(select(func.count(User.id)).where(User.department_id == dept.id)) or 0
        )

        act_filters = [Activity.user_id == User.id, User.department_id == dept.id]
        if year is not None:
            act_filters.append(extract("year", Activity.activity_date) == year)
        if month is not None:
            act_filters.append(extract("month", Activity.activity_date) == month)

        # Active users in department
        active_users = int(
            db.scalar(
                select(func.count(func.distinct(Activity.user_id)))
                .select_from(Activity)
                .join(User, Activity.user_id == User.id)
                .where(User.department_id == dept.id, *act_filters[2:])
            )
            or 0
        )

        # Total emissions in department
        total_emission = float(
            db.scalar(
                select(func.coalesce(func.sum(Activity.emission), 0.0))
                .select_from(Activity)
                .join(User, Activity.user_id == User.id)
                .where(User.department_id == dept.id, *act_filters[2:])
            )
            or 0.0
        )

        avg_per_active = (total_emission / active_users) if active_users > 0 else 0.0

        # Category breakdown for department
        cat_rows = db.execute(
            select(
                Activity.category,
                func.coalesce(func.sum(Activity.emission), 0.0).label("cat_tot"),
            )
            .select_from(Activity)
            .join(User, Activity.user_id == User.id)
            .where(User.department_id == dept.id, *act_filters[2:])
            .group_by(Activity.category)
        ).all()

        cat_map = {r.category.lower(): float(r.cat_tot) for r in cat_rows}
        categories = {
            cat: round(cat_map.get(cat, 0.0), 4)
            for cat in ["travel", "electricity", "food", "waste"]
        }

        dept_results.append(
            {
                "department": dept.name,
                "users": total_users,
                "active_users": active_users,
                "total_emission": round(total_emission, 4),
                "average_per_active_user": round(avg_per_active, 4),
                "categories": categories,
            }
        )

    return {"departments": dept_results}


def get_hostel_analytics(
    month: int | None,
    year: int | None,
    db: Session,
) -> dict[str, Any]:
    """Retrieve population, active user count, total emissions, average per user, and category breakdown per hostel."""
    hostels = db.scalars(select(Hostel).order_by(Hostel.name)).all()

    hostel_results = []
    for h in hostels:
        total_users = int(
            db.scalar(select(func.count(User.id)).where(User.hostel_id == h.id)) or 0
        )

        act_filters = []
        if year is not None:
            act_filters.append(extract("year", Activity.activity_date) == year)
        if month is not None:
            act_filters.append(extract("month", Activity.activity_date) == month)

        active_users = int(
            db.scalar(
                select(func.count(func.distinct(Activity.user_id)))
                .select_from(Activity)
                .join(User, Activity.user_id == User.id)
                .where(User.hostel_id == h.id, *act_filters)
            )
            or 0
        )

        total_emission = float(
            db.scalar(
                select(func.coalesce(func.sum(Activity.emission), 0.0))
                .select_from(Activity)
                .join(User, Activity.user_id == User.id)
                .where(User.hostel_id == h.id, *act_filters)
            )
            or 0.0
        )

        avg_per_active = (total_emission / active_users) if active_users > 0 else 0.0

        cat_rows = db.execute(
            select(
                Activity.category,
                func.coalesce(func.sum(Activity.emission), 0.0).label("cat_tot"),
            )
            .select_from(Activity)
            .join(User, Activity.user_id == User.id)
            .where(User.hostel_id == h.id, *act_filters)
            .group_by(Activity.category)
        ).all()

        cat_map = {r.category.lower(): float(r.cat_tot) for r in cat_rows}
        categories = {
            cat: round(cat_map.get(cat, 0.0), 4)
            for cat in ["travel", "electricity", "food", "waste"]
        }

        hostel_results.append(
            {
                "hostel": h.name,
                "users": total_users,
                "active_users": active_users,
                "total_emission": round(total_emission, 4),
                "average_per_active_user": round(avg_per_active, 4),
                "categories": categories,
            }
        )

    return {"hostels": hostel_results}


def get_user_benchmark(
    user_id: int,
    month: int | None,
    year: int | None,
    db: Session,
) -> dict[str, Any]:
    """Calculate user's footprint benchmark against the database-derived campus average per active user."""
    user = db.get(User, user_id)
    if not user:
        raise UserNotFoundError(f"User with ID {user_id} not found.")

    act_filters = []
    if year is not None:
        act_filters.append(extract("year", Activity.activity_date) == year)
    if month is not None:
        act_filters.append(extract("month", Activity.activity_date) == month)

    # 1. User emission
    stmt_user = select(func.coalesce(func.sum(Activity.emission), 0.0)).where(
        Activity.user_id == user_id, *act_filters
    )
    user_emission = float(db.scalar(stmt_user) or 0.0)

    # 2. Campus overview for benchmark comparison
    campus = get_campus_overview(month=month, year=year, db=db)
    campus_average = campus["average_per_active_user"]

    diff = user_emission - campus_average
    diff_pct = (diff / campus_average * 100.0) if campus_average > 0 else 0.0

    return {
        "user_id": user_id,
        "month": month,
        "year": year,
        "user_emission": round(user_emission, 4),
        "campus_average": round(campus_average, 4),
        "difference": round(diff, 4),
        "difference_percentage": round(diff_pct, 2),
        "benchmark_type": "Campus average per active user",
    }


def get_leaderboard(
    entity_type: str,
    month: int | None,
    year: int | None,
    db: Session,
) -> dict[str, Any]:
    """Generate leaderboard-ready entity aggregation distinguishing total emissions, per-user emissions, and period change."""
    clean_type = entity_type.strip().lower()
    if clean_type not in ("department", "hostel"):
        raise ValueError("Leaderboard type must be 'department' or 'hostel'.")

    # Determine current period and previous period
    now = datetime.now()
    curr_yr = year if year is not None else now.year
    curr_mo = month if month is not None else now.month

    # Calculate previous month for period-over-period comparison
    if curr_mo == 1:
        prev_mo = 12
        prev_yr = curr_yr - 1
    else:
        prev_mo = curr_mo - 1
        prev_yr = curr_yr

    if clean_type == "department":
        entities = get_department_analytics(month=curr_mo, year=curr_yr, db=db)["departments"]
        prev_entities = {
            e["department"]: e["total_emission"]
            for e in get_department_analytics(month=prev_mo, year=prev_yr, db=db)["departments"]
        }
        name_key = "department"
    else:
        entities = get_hostel_analytics(month=curr_mo, year=curr_yr, db=db)["hostels"]
        prev_entities = {
            e["hostel"]: e["total_emission"]
            for e in get_hostel_analytics(month=prev_mo, year=prev_yr, db=db)["hostels"]
        }
        name_key = "hostel"

    leaderboard_items = []
    for item in entities:
        name = item[name_key]
        curr_em = item["total_emission"]
        prev_em = prev_entities.get(name, 0.0)

        change_pct = (
            ((curr_em - prev_em) / prev_em * 100.0) if prev_em > 0 else 0.0
        )

        leaderboard_items.append(
            {
                "name": name,
                "users": item["users"],
                "active_users": item["active_users"],
                "total_emission": curr_em,
                "average_per_active_user": item["average_per_active_user"],
                "current_period_emission": curr_em,
                "previous_period_emission": prev_em,
                "change_percentage": round(change_pct, 2),
            }
        )

    # Sort leaderboard by average per active user ASC (lower carbon footprint per active user is better)
    leaderboard_items.sort(key=lambda x: x["average_per_active_user"])

    return {
        "entity_type": clean_type,
        "month": curr_mo,
        "year": curr_yr,
        "leaderboard": leaderboard_items,
    }
