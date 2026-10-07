from __future__ import annotations

from typing import Any, Callable, Optional
import customtkinter as ctk


class BrainDumpCard(ctk.CTkFrame):
    def __init__(
        self,
        master: Any,
        initial_text: str = "",
        on_change: Optional[Callable[[str], None]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, corner_radius=12, **kwargs)

        self.on_change = on_change
        self._save_timer: Optional[str] = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(
            master=self,
            text="BRAIN DUMP",
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, padx=16, pady=(10, 4), sticky="w")

        self.textbox = ctk.CTkTextbox(
            master=self,
            font=ctk.CTkFont(family="Arial", size=13),
            corner_radius=8,
            height=90,
            activate_scrollbars=False,
        )
        self.textbox.grid(row=1, column=0, padx=14, pady=(0, 12), sticky="nsew")

        if initial_text:
            self.textbox.insert("1.0", initial_text)

        self.textbox.bind("<KeyRelease>", lambda _e: self._on_text_modified())
        self.textbox.bind("<FocusOut>", lambda _e: self._trigger_immediate_save())

    def _on_text_modified(self) -> None:
        if self._save_timer is not None:
            self.after_cancel(self._save_timer)
        self._save_timer = self.after(500, self._trigger_immediate_save)

    def _trigger_immediate_save(self) -> None:
        self._save_timer = None
        if self.on_change:
            self.on_change(self.get_text())

    def get_text(self) -> str:
        return self.textbox.get("1.0", "end-1c")

    def set_text(self, text: str) -> None:
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", text)
