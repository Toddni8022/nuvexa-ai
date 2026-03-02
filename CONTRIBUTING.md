# Contributing to NUVEXA AI

Thank you for your interest in contributing! Here's how to get started.

---

## Development Setup

```bash
git clone https://github.com/Toddni8022/nuvexa-ai.git
cd nuvexa-ai
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows

pip install -r requirements.txt
pip install pytest pytest-cov ruff mypy
cp .env.example .env        # add your API key
```

---

## Workflow

1. **Fork** the repository and create a feature branch:
   ```bash
   git checkout -b feat/my-feature
   ```
2. Make your changes following the code style guidelines below.
3. **Test** your changes:
   ```bash
   make test
   ```
4. **Lint** your code:
   ```bash
   make lint
   ```
5. Open a **Pull Request** against `main` with a clear description.

---

## Code Style

- Formatted with **ruff** (`make format`)
- Type hints encouraged for all public functions
- Docstrings in Google style
- Line length: 100 characters

---

## Testing

All new features should be accompanied by tests in the `tests/` directory. Run:

```bash
make test          # with coverage
make test-fast     # without coverage
```

---

## Reporting Bugs

Open an issue on GitHub and include:

- Python version (`python --version`)
- Steps to reproduce
- Expected vs actual behaviour
- Relevant log output

---

## Feature Requests

Open an issue with the label `enhancement` and describe:

- The problem you are trying to solve
- Your proposed solution
- Any alternatives you have considered
