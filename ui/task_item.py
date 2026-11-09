from __future__ import annotations

from typing import Any, Callable, Dict, Optional
import customtkinter as ctk


class TaskItem(ctk.CTkFrame):
    def __init__(
            self,
            master: Any,
            task_data: Dict[str, Any],  # ZMENA: Prijímame celý slovník
            on_toggle: Optional[Callable[["TaskItem", bool], None]] = None,
            on_delete: Optional[Callable[["TaskItem"], None]] = None,
            **kwargs: Any,
    ) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)

        self.task_data = task_data  # Schováme si celý slovník na neskôr!

        # Vytiahneme text a stav, aby ich UI vedelo vykresliť
        self.text = self.task_data.get("text", "")
        self._completed = bool(self.task_data.get("completed", False))

        self.on_toggle = on_toggle
        self.on_delete = on_delete

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        self._check_var = ctk.BooleanVar(value=self._completed)
        self.checkbox = ctk.CTkCheckBox(
            master=self,
            text="",
            width=22,
            checkbox_width=18,
            checkbox_height=18,
            corner_radius=4,
            variable=self._check_var,
            command=self._handle_toggle,
        )
        self.checkbox.grid(row=0, column=0, padx=(4, 6), pady=3, sticky="w")

        self.label = ctk.CTkLabel(
            master=self,
            text=self.text,
            anchor="w",
            justify="left",
            wraplength=220,
            cursor="hand2",
        )
        self.label.grid(row=0, column=1, padx=(0, 6), pady=3, sticky="w")
        self.label.bind("<Button-1>", lambda _e: self._toggle_from_label())

        self.delete_btn = ctk.CTkButton(
            master=self,
            text="✕",
            width=22,
            height=22,
            corner_radius=6,
            fg_color="transparent",
            hover_color=("#ff4d4f", "#cf1322"),
            text_color=("gray60", "gray70"),
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._handle_delete,
        )
        self.delete_btn.grid(row=0, column=2, padx=(2, 4), pady=3, sticky="e")

        self._update_appearance()

    @property
    def completed(self) -> bool:
        return self._completed

    @completed.setter
    def completed(self, value: bool) -> None:
        self._completed = bool(value)
        self._check_var.set(self._completed)
        self._update_appearance()

    def _toggle_from_label(self) -> None:
        new_val = not self._completed
        self.set_completed(new_val)
        if self.on_toggle:
            self.on_toggle(self, self._completed)

    def _handle_toggle(self) -> None:
        self._completed = self._check_var.get()
        self._update_appearance()
        if self.on_toggle:
            self.on_toggle(self, self._completed)

    def _handle_delete(self) -> None:
        if self.on_delete:
            self.on_delete(self)

    def _update_appearance(self) -> None:
        if self._completed:
            self.label.configure(
                font=ctk.CTkFont(family="Arial", size=13, overstrike=True),
                text_color=("gray50", "gray55"),
            )
        else:
            self.label.configure(
                font=ctk.CTkFont(family="Arial", size=13, overstrike=False),
                text_color=("gray10", "gray95"),
            )

    def set_completed(self, completed: bool) -> None:
        self.completed = completed


    def get_data(self) -> Dict[str, Any]:
        self.task_data["text"] = self.text
        self.task_data["completed"] = self._completed
        return self.task_data