# NUVEXA AI

NUVEXA is a living AI assistant with real execution power. Unlike standard chatbots, NUVEXA doesn't just answer questions — it takes action. Built for Windows with a simple launcher, it runs four specialized AI modes from a single interface.

---

## Modes

| Mode | Description |
|------|-------------|
| **Assistant** | Planning, research, and task execution |
| **Shopping** | AI-native product search and checkout automation |
| **Therapist** | Emotional support and guided conversation |
| **Builder** | Project planning, architecture, and code generation |

---

## Key Features

- **Execution power** — Goes beyond chat to complete real tasks
- **AI-native shopping** — Product discovery through to checkout
- **Persistent history** — Cart, order history, and session memory stored in SQLite
- **Modern OpenAI integration** — Latest client API with full type hints and error handling
- **Windows-native** — One-click `.bat` launchers for setup and run

---

## Tech Stack

- **Python 3**
- **Streamlit** — Web interface
- **OpenAI GPT** — AI backbone
- **SQLite** — Persistent storage
- **Windows** — `.bat` launchers for easy startup

---

## Quick Start

### First time setup:
```
Double-click SETUP.bat
```

### Run NUVEXA:
```
Double-click RUN_NUVEXA.bat
```

Or manually:
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Requirements

- Python 3.11+
- OpenAI API key (set in `config.py`)
- Windows (recommended) or any OS with manual setup
