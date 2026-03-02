#!/usr/bin/env bash
# NUVEXA AI - Linux/macOS setup script
set -euo pipefail

echo ""
echo "  ========================================"
echo "        NUVEXA AI - Setup Wizard"
echo "  ========================================"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "  ERROR: python3 not found!"
    echo "  Install from https://www.python.org/downloads/ and re-run."
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "  Found: $PYTHON_VERSION"

# Upgrade pip
echo "  Upgrading pip..."
python3 -m pip install --upgrade pip --quiet

# Install dependencies
echo "  Installing dependencies..."
python3 -m pip install -r requirements.txt

echo ""
echo "  ========================================"
echo "  Setup Complete!"
echo "  ========================================"
echo ""
echo "  IMPORTANT: copy .env.example to .env and add your OpenAI API key."
echo "  Get one at: https://platform.openai.com/api-keys"
echo ""
echo "  Then run:  bash scripts/run.sh"
echo ""
