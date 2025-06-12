# 🤖 Interactive Physics Learning Bot

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)
![Framework](https://img.shields.io/badge/Framework-aiogram-blueviolet)
![Data Storage](https://img.shields.io/badge/Data-JSON-lightgrey)

A Telegram bot designed to make studying physics more engaging and structured.

---

## Features (Current Implementation)

- **Topic navigation:** Users can explore physics sections and subsections based on the structure defined in `themes.json`.
- **Access to theory:** The bot sends PDF notes compiled from LaTeX files for the selected topic.
- **Problem sets:** Each topic provides access to related tasks. The bot shows the number of available problems from `tasks.json`. (Automatic task delivery and answer validation are in progress.)
- **Reference materials:** The bot can send a file with physical constants and tabular data.
- **User-friendly navigation:** Includes a "Back" button to easily return to the previous menu level.

---

## Technical Overview

### Technologies Used

- **Language:** Python 3.11+
- **Framework:** [aiogram](https://github.com/aiogram/aiogram) — asynchronous framework for Telegram bots
- **Data storage:** JSON files (`themes.json`, `scripts.json`, `config.json`, `tasks.json`)
- **Educational content:** PDF files compiled from `.tex` sources

### Architecture Summary

- At startup, the bot reads configuration and content structure from JSON files.
- A custom `state` module tracks each user's current path through the topic hierarchy and stores their answers.
- Message handlers process `/start`, `/choose`, `/constants`, and interpret regular text as menu selections.
- `get_by_path` enables dynamic access to the correct portion of `themes.json` based on user navigation.
- `send_file` handles PDF delivery of theory and constants.
- The `keyboards` module builds context-aware reply keyboards based on available options.

---

## Project Structure

```bash
main.py                # Entry point

bot/                   # Core logic
├── bot.py             # Bot initialization
├── handlers.py        # Command/message handling
├── keyboards.py       # Dynamic keyboard generation
└── utils.py           # File sending, JSON loading, etc.

data/                  # Static content structure and config
├── config.json
├── themes.json
└── scripts.json

state/                 # User session/state management
├── storage.py
└── user_data.py

assets/                # Physics theory, tasks, and constants (PDF/TeX/JSON)
```

## Notes
* All theory materials are stored as LaTeX source files and compiled into PDFs.
* Tasks are organized per topic, with support for short image-based explanations.
* The bot is designed to be easily extended with new topics and problem sets.