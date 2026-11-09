from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional
import customtkinter as ctk

from ui.task_item import TaskItem
import time
import datetime


class PlannerCard(ctk.CTkFrame):
    def __init__(
        self,
        master: Any,
        title: str,
        initial_tasks: Optional[List[Dict[str, Any]]] = None,
        is_today: bool = False,
        on_change: Optional[Callable[[], None]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, corner_radius=12, **kwargs)

        self.title_text = title
        self.is_today = is_today
        self.on_change = on_change
        self.task_items: List[TaskItem] = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=12, pady=(10, 6), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=0)

        self.title_label = ctk.CTkLabel(
            master=self.header_frame,
            text=self.title_text,
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        self.badge_label: Optional[ctk.CTkLabel] = None
        if self.is_today:
            self._apply_today_badge()

        self.tasks_container = ctk.CTkScrollableFrame(
            master=self,
            fg_color="transparent",
            corner_radius=8,
        )
        self.tasks_container.grid(row=1, column=0, padx=6, pady=2, sticky="nsew")
        self.tasks_container.grid_columnconfigure(0, weight=1)

        self.add_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.add_frame.grid(row=2, column=0, padx=10, pady=(6, 10), sticky="ew")
        self.add_frame.grid_columnconfigure(0, weight=1)
        self.add_frame.grid_columnconfigure(1, weight=0)

        self.entry = ctk.CTkEntry(
            master=self.add_frame,
            placeholder_text="Nová úloha...",
            height=28,
            font=ctk.CTkFont(size=12),
        )
        self.entry.grid(row=0, column=0, padx=(0, 6), sticky="ew")
        self.entry.bind("<Return>", lambda _e: self._handle_add_task())

        self.add_btn = ctk.CTkButton(
            master=self.add_frame,
            text="+",
            width=30,
            height=28,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self._handle_add_task,
        )
        self.add_btn.grid(row=0, column=1, sticky="e")

        if initial_tasks:
            for task_data in initial_tasks:
                self.add_task(task_data=task_data, notify=False)

    def _apply_today_badge(self) -> None:
        if not self.badge_label:
            self.badge_label = ctk.CTkLabel(
                master=self.header_frame,
                text="DNES",
                font=ctk.CTkFont(family="Arial", size=10, weight="bold"),
                text_color="#ffffff",
                fg_color="#1f6aa5",
                corner_radius=6,
                padx=6,
                pady=2,
            )
            self.badge_label.grid(row=0, column=1, sticky="e")

    def update_title(self, new_title: str, is_today: bool = False) -> None:
        self.title_text = new_title
        self.title_label.configure(text=new_title)
        self.is_today = is_today
        if is_today:
            self._apply_today_badge()
        elif self.badge_label:
            self.badge_label.destroy()
            self.badge_label = None

    def _handle_add_task(self) -> None:
        text = self.entry.get().strip()
        if not text:
            return


        new_task_data = {
            "id": int(time.time() * 1000),
            "text": text,
            "completed": False,
            "priority": 1,
            "date": datetime.datetime.now().isocalendar().week,
            "year": datetime.datetime.now().isocalendar()[0]
        }

        self.add_task(task_data=new_task_data, notify=True)
        self.entry.delete(0, "end")


    def add_task(self, task_data: Dict[str, Any], notify: bool = True) -> None:
        task_item = TaskItem(
            master=self.tasks_container,
            task_data=task_data,  # Posielame celý slovník do TaskItem!
            on_toggle=self._on_task_toggle,
            on_delete=self._on_task_delete,
        )
        row_idx = len(self.task_items)
        task_item.grid(row=row_idx, column=0, pady=2, sticky="ew")
        self.task_items.append(task_item)

        if notify and self.on_change:
            self.on_change()


        def set_tasks_data(self, tasks_data: List[Dict[str, Any]]) -> None:
            for item in self.task_items:
                item.destroy()
            self.task_items.clear()

            for task_data in tasks_data:
                self.add_task(task_data=task_data, notify=False)

    def _on_task_toggle(self, _task_item: TaskItem, _completed: bool) -> None:
        if self.on_change:
            self.on_change()

    def _on_task_delete(self, task_item: TaskItem) -> None:
        if task_item in self.task_items:
            self.task_items.remove(task_item)
            task_item.destroy()
            self._regrid_tasks()
            if self.on_change:
                self.on_change()

    def _regrid_tasks(self) -> None:
        for idx, item in enumerate(self.task_items):
            item.grid(row=idx, column=0, pady=2, sticky="ew")

    def get_tasks_data(self) -> List[Dict[str, Any]]:
        return [item.get_data() for item in self.task_items]

    def set_tasks_data(self, tasks_data: List[Dict[str, Any]]) -> None:
        for item in self.task_items:
            item.destroy()
        self.task_items.clear()

        for task_data in tasks_data:
            self.add_task(task_data=task_data, notify=False)
