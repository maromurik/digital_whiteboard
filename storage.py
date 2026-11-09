from __future__ import annotations

import copy
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Union
import datetime



def load_tasks():
    if Path("data.json").exists():
        try:
            with open("data.json", "r", encoding="utf-8") as data:
                task_list = json.load(data)
        except ValueError:
            task_list = {
    "tasks": [],
    "brain_dump": "",
    "goal_of_the_week": {}
}
    else:
        task_list = {
    "tasks": [],
    "brain_dump": "",
    "goal_of_the_week": {}
}
    return task_list


def save_tasks(task_text,task_priority,task_category):
    data_dict = load_tasks()
    max_dict = max(data_dict["tasks"], key=lambda x: x["id"], default={"id": 0})
    id_append = max_dict["id"]
    task_par = {"id": id_append+1 ,"text" : task_text,"priority": task_priority,
                "is_checked": False,"date": datetime.datetime.now().isocalendar().week,
                "category":task_category}
    data_dict["tasks"].append(task_par)

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=4)
