from __future__ import annotations

import datetime
from typing import Any, Callable, Optional
import customtkinter as ctk

import time_service


class HeaderFrame(ctk.CTkFrame):
    def __init__(
        self,
        master: Any,
        title: str = "DIGITAL PLANNING WHITEBOARD",
        on_date_changed: Optional[Callable[[], None]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, corner_radius=12, **kwargs)

        self.title_text = title
        self.on_date_changed = on_date_changed
        self._last_day: int = datetime.date.today().day

        self.grid_columnconfigure(0, weight=1, uniform="header_side")
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1, uniform="header_side")

        self.left_container = ctk.CTkFrame(master=self, fg_color="transparent")
        self.left_container.grid(row=0, column=0, padx=25, pady=10, sticky="w")

        self.week_badge = ctk.CTkLabel(
            master=self.left_container,
            text=f"📅 {time_service.get_current_week_number()}. TÝŽDEŇ",
            font=ctk.CTkFont(family="Arial", size=13, weight="bold"),
            text_color=("gray45", "gray65"),
        )
        self.week_badge.pack(anchor="w")

        self.title_label = ctk.CTkLabel(
            master=self,
            text=self.title_text,
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            anchor="center",
            justify="center",
        )
        self.title_label.grid(row=0, column=1, padx=10, pady=(15, 15), sticky="ew")

        self.time_container = ctk.CTkFrame(master=self, fg_color="transparent")
        self.time_container.grid(row=0, column=2, padx=25, pady=10, sticky="e")

        self.clock_label = ctk.CTkLabel(
            master=self.time_container,
            text=time_service.get_current_time(),
            font=ctk.CTkFont(family="Consolas", size=26, weight="bold"),
            text_color=("#1f6aa5", "#3a8ed0"),
            anchor="e",
        )
        self.clock_label.grid(row=0, column=0, sticky="e")

        self.date_label = ctk.CTkLabel(
            master=self.time_container,
            text=time_service.get_current_date_formatted(),
            font=ctk.CTkFont(family="Arial", size=13),
            text_color=("gray40", "gray70"),
            anchor="e",
        )
        self.date_label.grid(row=1, column=0, sticky="e")

        self._tick()

    def _tick(self) -> None:
        current_time = time_service.get_current_time()
        self.clock_label.configure(text=current_time)

        today = datetime.date.today().day
        if today != self._last_day:
            self._last_day = today
            self.date_label.configure(text=time_service.get_current_date_formatted())
            self.week_badge.configure(text=f"📅 {time_service.get_current_week_number()}. TÝŽDEŇ")
            if self.on_date_changed:
                self.on_date_changed()

        self.after(1000, self._tick)
