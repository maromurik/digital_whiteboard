from __future__ import annotations

import copy
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Union

DEFAULT_STORAGE_FILE = Path(__file__).parent / "data.json"

DEFAULT_GOAL_DAYS = {
    "Pondelok": False,
    "Utorok": False,
    "Streda": False,
    "Štvrtok": False,
    "Piatok": False,
    "Sobota": False,
    "Nedeľa": False,
}

DEFAULT_DATA: Dict[str, Any] = {
    "goal_of_the_week": {
        "title": "GOAL OF THE WEEK",
        "text": "Pripraviť sa na labáky z TOI",
        "days": dict(DEFAULT_GOAL_DAYS),
    },
    "days": {
        "Pondelok": [
            {"text": "Ranný beh", "completed": False},
            {"text": "Stredomorský obed", "completed": False},
        ],
        "Utorok": [
            {"text": "Fitko (Bench + Drepy)", "completed": False},
            {"text": "Labáky TOI", "completed": False},
        ],
        "Streda": [
            {"text": "Opakovať Booleovu algebru", "completed": False},
        ],
        "Štvrtok": [
            {"text": "Fitko", "completed": False},
            {"text": "PyCharm projekt", "completed": False},
        ],
        "Piatok": [
            {"text": "Beh", "completed": False},
            {"text": "Zadanie č. 14 odovzdať", "completed": False},
        ],
        "Víkend": [
            {"text": "Oddych", "completed": False},
            {"text": "Plán na ďalší týždeň", "completed": False},
        ],
    },
    "recurring": {
        "DAILY": [
            {"text": "umyt zuby", "completed": False},
            {"text": "postel", "completed": False},
        ],
        "WEEKLY": [
            {"text": "weekly1", "completed": False},
            {"text": "weekly2", "completed": False},
        ],
        "YEARLY": [
            {"text": "yearly1", "completed": False},
            {"text": "yearly2", "completed": False},
        ],
    },
    "brain_dump": "braindumptext",
}


def _normalize_task_list(raw_tasks: Union[List[Any], Any]) -> List[Dict[str, Any]]:
    if not isinstance(raw_tasks, list):
        return []

    normalized = []
    for item in raw_tasks:
        if isinstance(item, str):
            normalized.append({"text": item, "completed": False})
        elif isinstance(item, dict):
            normalized.append({
                "text": str(item.get("text", "")),
                "completed": bool(item.get("completed", False)),
            })
    return normalized


def get_default_data() -> Dict[str, Any]:
    return copy.deepcopy(DEFAULT_DATA)


def load_data(filepath: Union[str, Path] | None = None) -> Dict[str, Any]:
    path = Path(filepath) if filepath is not None else DEFAULT_STORAGE_FILE

    if not path.exists():
        initial = get_default_data()
        save_data(initial, path)
        return initial

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        default = get_default_data()

        if "goal_of_the_week" not in data or not isinstance(data["goal_of_the_week"], dict):
            data["goal_of_the_week"] = default["goal_of_the_week"]
        else:
            gotw = data["goal_of_the_week"]
            if "text" not in gotw:
                old_tasks = gotw.get("tasks", [])
                if old_tasks and isinstance(old_tasks, list):
                    first_task = old_tasks[0]
                    gotw["text"] = first_task.get("text", "") if isinstance(first_task, dict) else str(first_task)
                else:
                    gotw["text"] = default["goal_of_the_week"]["text"]

            if "days" not in gotw or not isinstance(gotw["days"], dict):
                gotw["days"] = dict(DEFAULT_GOAL_DAYS)
            else:
                for day_name in DEFAULT_GOAL_DAYS:
                    if day_name not in gotw["days"]:
                        gotw["days"][day_name] = False

        if "days" not in data or not isinstance(data["days"], dict):
            data["days"] = default["days"]
        else:
            for day in default["days"]:
                if day not in data["days"]:
                    data["days"][day] = default["days"][day]
                else:
                    data["days"][day] = _normalize_task_list(data["days"][day])

        if "recurring" not in data or not isinstance(data["recurring"], dict):
            data["recurring"] = default["recurring"]
        else:
            for rec in default["recurring"]:
                if rec not in data["recurring"]:
                    data["recurring"][rec] = default["recurring"][rec]
                else:
                    data["recurring"][rec] = _normalize_task_list(data["recurring"][rec])

        if "brain_dump" not in data or not isinstance(data["brain_dump"], str):
            data["brain_dump"] = default["brain_dump"]

        return data

    except Exception as e:
        fallback = get_default_data()
        save_data(fallback, path)
        return fallback


def save_data(data: Dict[str, Any], filepath: Union[str, Path] | None = None) -> bool:
    path = Path(filepath) if filepath is not None else DEFAULT_STORAGE_FILE

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_suffix(".tmp")
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        temp_path.replace(path)
        return True
    except Exception as e:
        return False
