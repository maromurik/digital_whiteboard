# 📋 Digital Planning Whiteboard

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet)](https://github.com/TomSchimansky/CustomTkinter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](#)

A sleek, dark-themed **Digital Planning Whiteboard** and personal productivity dashboard built with Python and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter). Designed to replicate the intuitive feel of a physical planning board while leveraging dynamic date tracking, modular UI components, and safe state auto-persistence.

---

## ✨ Features

- **🕒 Dynamic Header & Live Clock:**
  - Real-time digital clock with 1-second auto-refresh.
  - Centered modern title with current date, day name, and ISO week number.
  - Automatic midnight rollover updating calendar dates on the fly.

- **🎯 Goal of the Week & 7-Day Habit Tracker:**
  - Centered weekly primary objective input with inline editing.
  - 7 individual daily checkboxes (Monday through Sunday) with dynamic dates to track consistency throughout the week.
  - Visual highlight for the current day.

- **📅 Weekly Planner with Dynamic Dates:**
  - 6 dedicated columns: *Pondelok* (Monday) through *Piatok* (Friday) + *Víkend* (Weekend).
  - Dates calculated dynamically using `datetime` relative to the current week.
  - Prominent **DNES** (Today) badge indicating the current active day.

- **🔄 Recurring Routines:**
  - Structured columns for recurring commitments: **DAILY**, **WEEKLY**, and **YEARLY**.

- **✅ Interactive Reusable Tasks (`TaskItem`):**
  - Checkbox toggle with instant visual feedback (strikethrough text and contrast dimming).
  - One-click deletion (`✕`) with automated UI reordering.
  - Inline input bar (`+`) for quickly appending new tasks to any section.

- **💡 Distraction-Free Brain Dump:**
  - Full-width, multi-line quick-notes area without cluttering scrollbars.
  - Auto-saves changes with smart typing debouncing (500 ms).

- **💾 Safe Auto-Persistence (`storage.py`):**
  - Saves all tasks, checkbox states, and free-form notes directly to `data.json`.
  - Atomic file writes using temporary swap files to prevent file corruption on crashes or unexpected shutdowns.
  - Automatic data normalization and backward compatibility.

---

## 🏗️ Project Architecture

The application is structured into clean, decoupled layers following modular software design principles:

```text
digital_whiteboard/
├── data.json              # Local persistent storage (JSON)
├── main.py                # Main application entry point & layout coordinator
├── requirements.txt       # Project dependencies
├── storage.py             # Data persistence layer (load / atomic save / defaults)
├── time_service.py        # Date & time calculation service (datetime helpers)
└── ui/                    # Reusable CustomTkinter UI components
    ├── __init__.py        # Package initialization & component exports
    ├── brain_dump_card.py # Brain Dump card without scrollbar
    ├── goal_card.py       # Centered Goal of the Week with 7-day checkboxes
    ├── header.py          # Balanced header with live clock & dynamic date
    ├── planner_card.py    # Reusable card component for day columns & routines
    └── task_item.py       # Reusable task widget (checkbox, text, delete button)
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed on your system.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/digital_whiteboard.git
   cd digital_whiteboard
   ```

2. **Create and activate a virtual environment:**
   - **Windows:**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\activate
     ```
   - **Linux / macOS:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application:**
   ```bash
   python main.py
   ```

---

## 🛠️ Tech Stack

- **Language:** [Python 3](https://www.python.org/)
- **UI Framework:** [CustomTkinter](https://customtkinter.tomschimansky.com/) (modern extension of Tkinter)
- **Time Engine:** Python Standard Library (`datetime`)
- **Persistence:** JSON with atomic file substitution

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
