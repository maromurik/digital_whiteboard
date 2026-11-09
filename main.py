from __future__ import annotations

from typing import Dict
import customtkinter as ctk
from storage import load_tasks, save_tasks
import time_service
from ui import BrainDumpCard, GoalCard, HeaderFrame, PlannerCard
import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class DigitalWhiteboardApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("DIGITAL PLANNING WHITEBOARD")
        self.geometry("1600x950+0+0")
        self.minsize(1200, 750)

        self.data: dict = load_tasks()

        self.day_cards: Dict[str, PlannerCard] = {}
        self.recurring_cards: Dict[str, PlannerCard] = {}
        self.zobrazeny_tyzden = datetime.datetime.now().isocalendar().week
        self.zobrazeny_rok = datetime.datetime.now().isocalendar()[0]

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
            current_viewed_week=self.zobrazeny_tyzden,
            on_prev_week=self.posun_dozadu,
            on_next_week=self.posun_dopredu
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
        planner_headers = time_service.get_all_planner_headers()
        ordered_days = ["Pondelok", "Utorok", "Streda", "Štvrtok", "Piatok", "Víkend"]

        for idx, day_key in enumerate(ordered_days):
            row = (idx // 3) + 2
            col = idx % 3

            initial_tasks = [
                uloha for uloha in self.data.get("tasks", [])
                if uloha.get("category") == day_key and uloha.get("date") == self.zobrazeny_tyzden and uloha.get("year", 2026) == self.zobrazeny_rok
            ]

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
        categories = ["DAILY", "WEEKLY", "YEARLY"]

        for col, cat_key in enumerate(categories):
            initial_tasks = [uloha for uloha in self.data.get("tasks", []) if uloha.get("category") == cat_key]

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
        ref_datum = time_service.get_date_from_week(self.zobrazeny_tyzden, self.zobrazeny_rok)
        headers = time_service.get_all_planner_headers(ref_datum)


        aktualny_tyzden = datetime.datetime.now().isocalendar().week

        for day_key, card in self.day_cards.items():
            new_title = headers.get(day_key, day_key)

            ukaz_dnes = (self.zobrazeny_tyzden == aktualny_tyzden) and time_service.is_today(day_key)

            card.update_title(new_title, is_today=ukaz_dnes)

    def posun_dozadu(self) -> None:
        self.save_all()
        self.zobrazeny_tyzden -= 1

        if self.zobrazeny_tyzden < 1:
            self.zobrazeny_tyzden = 52
            self.zobrazeny_rok -= 1  # <--- PRECHOD DO MINULÉHO ROKA

        self.header.update_week_text(self.zobrazeny_tyzden)
        self._obnov_zobrazenie_tyzdna()

    def posun_dopredu(self) -> None:
        self.save_all()
        self.zobrazeny_tyzden += 1

        if self.zobrazeny_tyzden > 52:
            self.zobrazeny_tyzden = 1
            self.zobrazeny_rok += 1  # <--- PRECHOD DO ĎALŠIEHO ROKA

        self.header.update_week_text(self.zobrazeny_tyzden)
        self._obnov_zobrazenie_tyzdna()

    def _obnov_zobrazenie_tyzdna(self) -> None:
        self.data = load_tasks()
        self.update_planner_dates()

        for day_key, card in self.day_cards.items():
            nove_ulohy = [
                uloha for uloha in self.data.get("tasks", [])
                if uloha.get("category") == day_key and uloha.get("date") == self.zobrazeny_tyzden and uloha.get("year", 2026) == self.zobrazeny_rok
            ]
            card.set_tasks_data(nove_ulohy)

    def save_all(self) -> None:
        vsetky_ulohy = []

        for u in self.data.get("tasks", []):
            kat = u.get("category")
            datum = u.get("date")
            rok = u.get("year", 2026)  # Pridané načítanie roku

            if kat in ["DAILY", "WEEKLY", "YEARLY"]:
                continue

            # Pridaná kontrola: preskoč len ak sedí týždeň AJ rok
            if datum == self.zobrazeny_tyzden and rok == self.zobrazeny_rok:
                continue

            vsetky_ulohy.append(u)

        for day_key, card in self.day_cards.items():
            ulohy_z_karty = card.get_tasks_data()
            for u in ulohy_z_karty:
                u["category"] = day_key
                u["date"] = self.zobrazeny_tyzden
                u["year"] = self.zobrazeny_rok  # Pridané ukladanie roku
                vsetky_ulohy.append(u)

        for cat_key, card in self.recurring_cards.items():
            ulohy_z_karty = card.get_tasks_data()
            for u in ulohy_z_karty:
                u["category"] = cat_key
                vsetky_ulohy.append(u)

        self.data["tasks"] = vsetky_ulohy
        self.data["goal_of_the_week"] = self.gotw_card.get_data()
        self.data["brain_dump"] = self.brain_dump_card.get_text()

        import json
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

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