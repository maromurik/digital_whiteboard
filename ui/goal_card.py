from __future__ import annotations

from typing import Any, Callable, Dict, Optional
import customtkinter as ctk

import time_service

DAYS_ORDER = ["Pondelok", "Utorok", "Streda", "Štvrtok", "Piatok", "Sobota", "Nedeľa"]


class GoalCard(ctk.CTkFrame):
    def __init__(
        self,
        master: Any,
        title: str = "GOAL OF THE WEEK",
        task_text: str = "Pripraviť sa na labáky z TOI",
        days_state: Optional[Dict[str, bool]] = None,
        on_change: Optional[Callable[[], None]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, corner_radius=12, **kwargs)

        self.title_text = title
        self.on_change = on_change
        self._debounce_timer: Optional[str] = None

        self.title_label = ctk.CTkLabel(
            master=self,
            text=self.title_text,
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            anchor="center",
            justify="center",
        )
        self.title_label.pack(side="top", pady=(12, 6))

        self.task_entry = ctk.CTkEntry(
            master=self,
            font=ctk.CTkFont(family="Arial", size=14, weight="normal"),
            justify="center",
            placeholder_text="Zadaj cieľ týždňa...",
            height=34,
            width=550,
        )
        self.task_entry.pack(side="top", pady=(0, 10))
        if task_text:
            self.task_entry.insert(0, task_text)

        self.task_entry.bind("<KeyRelease>", lambda _e: self._on_text_modified())
        self.task_entry.bind("<FocusOut>", lambda _e: self._trigger_change())

        self.checkboxes_container = ctk.CTkFrame(master=self, fg_color="transparent")
        self.checkboxes_container.pack(side="top", pady=(0, 14))

        self.checkbox_vars: Dict[str, ctk.BooleanVar] = {}
        self.checkbox_widgets: Dict[str, ctk.CTkCheckBox] = {}

        initial_days = days_state or {}
        week_dates = time_service.get_week_dates()

        for day in DAYS_ORDER:
            is_checked = bool(initial_days.get(day, False))
            var = ctk.BooleanVar(value=is_checked)
            self.checkbox_vars[day] = var

            day_date = week_dates.get(day)
            date_str = day_date.strftime("%d.%m.") if day_date else ""
            checkbox_label = f"{day} ({date_str})" if date_str else day

            is_today = time_service.is_today(day)

            cb = ctk.CTkCheckBox(
                master=self.checkboxes_container,
                text=checkbox_label,
                variable=var,
                command=self._on_checkbox_toggle,
                checkbox_width=20,
                checkbox_height=20,
                border_width=2,
                corner_radius=4,
                font=ctk.CTkFont(
                    family="Arial",
                    size=12,
                    weight="bold" if is_today else "normal",
                ),
                text_color=("#1f6aa5", "#3a8ed0") if is_today else ("gray10", "gray90"),
            )
            cb.pack(side="left", padx=7, pady=4)
            self.checkbox_widgets[day] = cb

    def _on_checkbox_toggle(self) -> None:
        self._trigger_change()

    def _on_text_modified(self) -> None:
        if self._debounce_timer is not None:
            self.after_cancel(self._debounce_timer)
        self._debounce_timer = self.after(500, self._trigger_change)

    def _trigger_change(self) -> None:
        self._debounce_timer = None
        if self.on_change:
            self.on_change()

    def get_task_text(self) -> str:
        return self.task_entry.get().strip()

    def get_days_state(self) -> Dict[str, bool]:
        return {day: self.checkbox_vars[day].get() for day in DAYS_ORDER}

    def get_data(self) -> Dict[str, Any]:
        return {
            "title": self.title_text,
            "text": self.get_task_text(),
            "days": self.get_days_state(),
        }

    def update_dynamic_dates(self) -> None:
        week_dates = time_service.get_week_dates()
        for day in DAYS_ORDER:
            day_date = week_dates.get(day)
            date_str = day_date.strftime("%d.%m.") if day_date else ""
            checkbox_label = f"{day} ({date_str})" if date_str else day
            is_today = time_service.is_today(day)

            if day in self.checkbox_widgets:
                self.checkbox_widgets[day].configure(
                    text=checkbox_label,
                    font=ctk.CTkFont(
                        family="Arial",
                        size=12,
                        weight="bold" if is_today else "normal",
                    ),
                    text_color=("#1f6aa5", "#3a8ed0") if is_today else ("gray10", "gray90"),
                )
