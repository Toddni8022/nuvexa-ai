# NUVEXA AI

![Python](https://img.shields.io/badge/python-3.11%2B-blue?logo=python)
![License](https://img.shields.io/badge/license-MIT-green)
![CI](https://github.com/Toddni8022/nuvexa-ai/actions/workflows/ci.yml/badge.svg)
![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-ff4b4b?logo=streamlit)

**NUVEXA** is a living AI assistant with real execution power. Unlike standard chatbots, NUVEXA doesn't just answer questions — it takes action. It runs four specialised AI modes from a single browser-based interface and persists your cart, orders, and conversation history across sessions.

---

## Features

| Feature | Description |
|---------|-------------|
| 🤖 **Assistant Mode** | General help, planning, and research |
| 🛒 **Shopping Mode** | AI-native product discovery and checkout |
| 💭 **Therapist Mode** | Emotional support and active listening |
| 🏗️ **Builder Mode** | Project planning, materials, and architecture |
| 💾 **Persistent history** | Cart, orders, and chats stored in SQLite |
| 🔄 **Session memory** | Conversation context carried across messages |
| 🌐 **Cross-platform** | Runs on Windows, macOS, and Linux |

---

## Architecture Overview

```
Browser (Streamlit UI)
       │
   app.py  ──────────────────┐
       │                     │
 assistant.py          database.py
 (OpenAI GPT)          (SQLite)
       │
 shopping.py
 (product catalogue)
```

See [`docs/architecture.md`](docs/architecture.md) for the full data-flow diagram.

---

## Prerequisites

- Python 3.11 or higher
- An [OpenAI API key](https://platform.openai.com/api-keys)
- Internet connection

---

## Installation

### Windows (quick start)

```bat
SETUP.bat
```

### Linux / macOS

```bash
bash scripts/setup.sh
```

### Manual

```bash
git clone https://github.com/Toddni8022/nuvexa-ai.git
cd nuvexa-ai
pip install -r requirements.txt
cp .env.example .env   # then add your OPENAI_API_KEY
```

---

## Quick Start

1. Configure your API key in `.env`:
   ```ini
   OPENAI_API_KEY=sk-...your-key...
   ```
2. Run the app:
   ```bash
   # Windows
   RUN_NUVEXA.bat

   # Linux / macOS
   bash scripts/run.sh

   # Any platform
   streamlit run app.py
   ```
3. Open <http://localhost:8501> in your browser.

For detailed instructions, see [`docs/setup.md`](docs/setup.md).

---

## Configuration

All configuration is driven by environment variables. Copy `.env.example` to `.env`:

```ini
# Required
OPENAI_API_KEY=sk-...your-key...
```

---

## Available Modes

Switch modes from the sidebar at any time:

| Mode | Icon | Best for |
|------|------|---------|
| Assistant | 🤖 | Questions, research, task planning |
| Shopping | 🛒 | Finding and buying products |
| Therapist | 💭 | Emotional support and reflection |
| Builder | 🏗️ | PC builds, home projects, planning |

---

## Docker

```bash
# Build and start
docker compose up --build

# Stop
docker compose down
```

---

## Project Structure

```
nuvexa-ai/
├── app.py               # Streamlit UI (entry point)
├── assistant.py         # AI assistant (OpenAI wrapper)
├── database.py          # SQLite persistence layer
├── shopping.py          # Product search engine
├── config.py            # Configuration and constants
├── requirements.txt     # Runtime dependencies
├── pyproject.toml       # Build & tool configuration
├── Makefile             # Developer shortcuts
├── Dockerfile           # Container image
├── docker-compose.yml   # Multi-service stack
├── .env.example         # Environment variable template
├── tests/               # Pytest test suite
├── docs/                # Documentation
└── scripts/             # Platform setup/run scripts
```

---

## Development

```bash
# Install dev dependencies
make setup

# Run tests
make test

# Lint
make lint

# Format
make format
```

---

## Roadmap

- [ ] Real e-commerce API integrations (Amazon, eBay)
- [ ] Voice input / text-to-speech output
- [ ] Multi-user accounts with authentication
- [ ] Plugin system for custom AI modes
- [ ] Mobile-optimised layout

---

## Contributing

We welcome contributions! See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

---

## License

This project is licensed under the [MIT License](LICENSE).
