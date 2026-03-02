# NUVEXA AI — Setup Guide

This guide walks you through installing and running NUVEXA on any platform.

---

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.11 | 3.12 |
| pip | 23.0 | latest |
| RAM | 512 MB | 1 GB |
| OpenAI API key | Required | — |

---

## Installation

### Windows (quick)

```bat
SETUP.bat
```

This script upgrades pip, installs all dependencies from `requirements.txt`, and guides you to configure your API key.

### Linux / macOS (quick)

```bash
bash scripts/setup.sh
```

### Manual (all platforms)

```bash
# 1. Clone the repository
git clone https://github.com/Toddni8022/nuvexa-ai.git
cd nuvexa-ai

# 2. (Optional) Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# or:  .venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and set OPENAI_API_KEY
```

---

## Configuration

Copy `.env.example` to `.env` and fill in the values:

```ini
OPENAI_API_KEY=sk-...your-key...
```

Obtain a key from <https://platform.openai.com/api-keys>.

---

## Running the Application

### Windows

```bat
RUN_NUVEXA.bat
```

### Linux / macOS

```bash
bash scripts/run.sh
```

### Manual

```bash
streamlit run app.py
```

The browser will open automatically at <http://localhost:8501>.

---

## Docker

```bash
# Build and start
docker compose up --build

# Stop
docker compose down
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Python not found | Install from <https://python.org/downloads> and add to PATH |
| API key rejected | Verify the key at <https://platform.openai.com/api-keys> |
| Port already in use | Run `streamlit run app.py --server.port 8502` |
| Module not found | Re-run `pip install -r requirements.txt` |
