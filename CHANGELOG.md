# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added
- `nuvexa_ai/__init__.py` — package initialisation with version metadata
- `tests/` — pytest test suite covering assistant, database, shopping, and config modules
- `docs/` — documentation for setup, assistant, shopping, database, architecture, and API
- `scripts/setup.sh` and `scripts/run.sh` — Linux/macOS equivalents of the Windows `.bat` launchers
- `scripts/README.md` — script usage guide
- `LICENSE` — MIT licence
- `CONTRIBUTING.md` — contribution guidelines
- `pyproject.toml` — full project metadata, ruff, mypy, pytest, and coverage configuration
- `setup.py` — editable-install compatibility shim
- `.editorconfig` — consistent editor settings across platforms
- `pytest.ini` — pytest configuration
- `.coveragerc` — coverage configuration
- `Makefile` — developer shortcuts (`setup`, `test`, `lint`, `format`, `run`, `docker-build`, `clean`)
- `Dockerfile` — container image for the Streamlit application
- `docker-compose.yml` — single-service stack with persistent volume
- `.dockerignore` — minimal Docker build context
- `.env.example` — environment variable template
- `.github/workflows/ci.yml` — CI pipeline: ruff lint, pytest (Python 3.11 & 3.12), mypy

### Changed
- `README.md` — enhanced with badges, architecture overview, installation guide (Windows + Linux/macOS), Docker instructions, project structure, roadmap, and contributing section
- `.gitignore` — expanded to cover coverage reports, mypy/ruff caches, and common OS/IDE files

---

## [1.0.0] — Initial Release

### Added
- Four AI modes: Assistant, Shopping, Therapist, Builder
- SQLite persistence for conversations, cart, and orders
- Streamlit web interface with sidebar navigation
- OpenAI GPT integration with model fallback (`gpt-4o` → `gpt-4` → `gpt-3.5-turbo`)
- Product catalogue search engine (ShoppingEngine)
- Windows `.bat` launchers (SETUP.bat, RUN_NUVEXA.bat)
