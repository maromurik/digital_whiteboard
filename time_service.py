from __future__ import annotations

import datetime
from typing import Dict, List, Tuple

SLOVAK_DAY_NAMES: List[str] = [
    "Pondelok",
    "Utorok",
    "Streda",
    "Štvrtok",
    "Piatok",
    "Sobota",
    "Nedeľa",
]

SLOVAK_MONTH_NAMES: List[str] = [
    "januára",
    "februára",
    "marca",
    "apríla",
    "mája",
    "júna",
    "júla",
    "augusta",
    "septembra",
    "októbra",
    "novembra",
    "decembra",
]


def get_current_time(include_seconds: bool = True) -> str:
    fmt = "%H:%M:%S" if include_seconds else "%H:%M"
    return datetime.datetime.now().strftime(fmt)


def get_current_date_formatted() -> str:
    today = datetime.date.today()
    day_name = SLOVAK_DAY_NAMES[today.weekday()]
    month_name = SLOVAK_MONTH_NAMES[today.month - 1]
    return f"{day_name}, {today.day}. {month_name} {today.year}"


def get_current_week_number() -> int:
    return datetime.date.today().isocalendar()[1]


def get_monday_of_week(ref_date: datetime.date | None = None) -> datetime.date:
    base = ref_date if ref_date is not None else datetime.date.today()
    return base - datetime.timedelta(days=base.weekday())


def get_week_day_date(day_index: int, ref_date: datetime.date | None = None) -> datetime.date:
    monday = get_monday_of_week(ref_date)
    return monday + datetime.timedelta(days=day_index)


def get_week_dates(ref_date: datetime.date | None = None) -> Dict[str, datetime.date]:
    monday = get_monday_of_week(ref_date)
    return {
        SLOVAK_DAY_NAMES[i]: monday + datetime.timedelta(days=i)
        for i in range(7)
    }


def format_day_header(day_key: str, ref_date: datetime.date | None = None) -> str:
    monday = get_monday_of_week(ref_date)
    day_mapping = {
        "Pondelok": monday,
        "Utorok": monday + datetime.timedelta(days=1),
        "Streda": monday + datetime.timedelta(days=2),
        "Štvrtok": monday + datetime.timedelta(days=3),
        "Piatok": monday + datetime.timedelta(days=4),
        "Sobota": monday + datetime.timedelta(days=5),
        "Nedeľa": monday + datetime.timedelta(days=6),
    }

    if day_key == "Víkend":
        sat = day_mapping["Sobota"]
        sun = day_mapping["Nedeľa"]
        return f"Víkend {sat.strftime('%d.%m.')} - {sun.strftime('%d.%m.')}"

    if day_key in day_mapping:
        d = day_mapping[day_key]
        return f"{day_key} {d.strftime('%d.%m.')}"

    return day_key


def get_all_planner_headers(ref_date: datetime.date | None = None) -> Dict[str, str]:
    days = ["Pondelok", "Utorok", "Streda", "Štvrtok", "Piatok", "Víkend"]
    return {day: format_day_header(day, ref_date) for day in days}


def is_today(day_key: str, ref_date: datetime.date | None = None) -> bool:
    today = ref_date if ref_date is not None else datetime.date.today()
    weekday = today.weekday()

    if day_key == "Víkend":
        return weekday in (5, 6)

    day_indices = {
        "Pondelok": 0,
        "Utorok": 1,
        "Streda": 2,
        "Štvrtok": 3,
        "Piatok": 4,
        "Sobota": 5,
        "Nedeľa": 6,
    }
    return day_indices.get(day_key) == weekday
