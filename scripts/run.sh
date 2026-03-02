#!/usr/bin/env bash
# NUVEXA AI - Linux/macOS run script
set -euo pipefail

echo ""
echo "  ========================================"
echo "        NUVEXA AI Assistant"
echo "  ========================================"
echo ""

if ! command -v python3 &>/dev/null; then
    echo "  ERROR: python3 not found! Run scripts/setup.sh first."
    exit 1
fi

echo "  Starting NUVEXA..."
echo "  The app will open at http://localhost:8501"
echo "  Press Ctrl+C to stop."
echo "  ========================================"
echo ""

python3 -m streamlit run app.py
