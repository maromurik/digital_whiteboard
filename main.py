from __future__ import annotations

from typing import Dict
import customtkinter as ctk

import storage
import time_service
from ui import BrainDumpCard, GoalCard, HeaderFrame, PlannerCard

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class DigitalWhiteboardApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("DIGITAL PLANNING WHITEBOARD")
        self.geometry("1600x950")
        self.minsize(1200, 750)

        self.data: dict = storage.load_data()

        self.day_cards: Dict[str, PlannerCard] = {}
        self.recurring_cards: Dict[str, PlannerCard] = {}

        self._setup_layout_grid()

        self._build_header()
        self._build_goal_of_the_week()
        self._build_weekly_planner()
        self._build_recurring_tasks()
        self._build_brain_dump()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_layout_grid(self) -> None:
        for col in range(3):
            self.grid_columnconfigure(col, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0, minsize=140)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=0, minsize=120)

    def _build_header(self) -> None:
        self.header = HeaderFrame(
            master=self,
            title="DIGITAL PLANNING WHITEBOARD",
            on_date_changed=self.update_planner_dates,
        )
        self.header.grid(row=0, column=0, columnspan=3, padx=16, pady=(14, 8), sticky="ew")

    def _build_goal_of_the_week(self) -> None:
        gotw_data = self.data.get("goal_of_the_week", {})
        task_text = gotw_data.get("text", "Pripraviť sa na labáky z TOI")
        days_state = gotw_data.get("days", {})

        self.gotw_card = GoalCard(
            master=self,
            title="GOAL OF THE WEEK",
            task_text=task_text,
            days_state=days_state,
            on_change=self.save_all,
        )
        self.gotw_card.grid(row=1, column=0, columnspan=3, padx=16, pady=6, sticky="nsew")

    def _build_weekly_planner(self) -> None:
        days_data = self.data.get("days", {})
        planner_headers = time_service.get_all_planner_headers()

        ordered_days = ["Pondelok", "Utorok", "Streda", "Štvrtok", "Piatok", "Víkend"]

        for idx, day_key in enumerate(ordered_days):
            row = (idx // 3) + 2
            col = idx % 3

            initial_tasks = days_data.get(day_key, [])
            header_title = planner_headers.get(day_key, day_key)
            is_cur_day = time_service.is_today(day_key)

            card = PlannerCard(
                master=self,
                title=header_title,
                initial_tasks=initial_tasks,
                is_today=is_cur_day,
                on_change=self.save_all,
            )
            card.grid(row=row, column=col, padx=8, pady=6, sticky="nsew")
            self.day_cards[day_key] = card

    def _build_recurring_tasks(self) -> None:
        recurring_data = self.data.get("recurring", {})
        categories = ["DAILY", "WEEKLY", "YEARLY"]

        for col, cat_key in enumerate(categories):
            initial_tasks = recurring_data.get(cat_key, [])
            card = PlannerCard(
                master=self,
                title=f"🔄 {cat_key}",
                initial_tasks=initial_tasks,
                on_change=self.save_all,
            )
            card.grid(row=4, column=col, padx=8, pady=6, sticky="nsew")
            self.recurring_cards[cat_key] = card

    def _build_brain_dump(self) -> None:
        initial_text = self.data.get("brain_dump", "")
        self.brain_dump_card = BrainDumpCard(
            master=self,
            initial_text=initial_text,
            on_change=lambda _text: self.save_all(),
        )
        self.brain_dump_card.grid(row=5, column=0, columnspan=3, padx=16, pady=(6, 14), sticky="nsew")

    def update_planner_dates(self) -> None:
        headers = time_service.get_all_planner_headers()
        for day_key, card in self.day_cards.items():
            new_title = headers.get(day_key, day_key)
            card.update_title(new_title, is_today=time_service.is_today(day_key))

        if hasattr(self, "gotw_card"):
            self.gotw_card.update_dynamic_dates()

    def save_all(self) -> None:
        self.data["goal_of_the_week"] = self.gotw_card.get_data()

        self.data["days"] = {
            day_key: card.get_tasks_data()
            for day_key, card in self.day_cards.items()
        }

        self.data["recurring"] = {
            cat_key: card.get_tasks_data()
            for cat_key, card in self.recurring_cards.items()
        }

        self.data["brain_dump"] = self.brain_dump_card.get_text()

        storage.save_data(self.data)

    def _on_close(self) -> None:
        try:
            self.save_all()
        finally:
            self.destroy()


def main() -> None:
    app = DigitalWhiteboardApp()
    app.mainloop()


if __name__ == "__main__":
    main()
