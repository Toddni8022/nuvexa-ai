"""Test script to verify setup is correct"""

import sys
from pathlib import Path

print("=" * 60)
print("Misinformation Debunking Copilot - Setup Test")
print("=" * 60)
print()

# Test Python version
print(f"✓ Python version: {sys.version}")
if sys.version_info < (3, 11):
    print("⚠ Warning: Python 3.11+ recommended")
print()

# Test imports
print("Testing imports...")
try:
    import streamlit
    print(f"✓ Streamlit {streamlit.__version__}")
except ImportError as e:
    print(f"✗ Streamlit: {e}")

try:
    from playwright.sync_api import sync_playwright
    print("✓ Playwright installed")
except ImportError as e:
    print(f"✗ Playwright: {e}")

try:
    import dotenv
    print("✓ python-dotenv installed")
except ImportError as e:
    print(f"✗ python-dotenv: {e}")

try:
    import pyperclip
    print("✓ pyperclip installed")
except ImportError as e:
    print(f"✗ pyperclip: {e}")

print()

# Test app modules
print("Testing app modules...")
try:
    from app.config import Config, SCREENSHOTS_DIR, DB_PATH
    print(f"✓ config.py - DB path: {DB_PATH}")
except Exception as e:
    print(f"✗ config.py: {e}")

try:
    from app.storage import get_storage
    storage = get_storage()
    stats = storage.get_stats()
    print(f"✓ storage.py - Database initialized. Total posts: {stats['total']}")
except Exception as e:
    print(f"✗ storage.py: {e}")

try:
    from app.scoring import MisinfoScorer
    scorer = MisinfoScorer()
    test_result = scorer.score_post("This is a test post.")
    print(f"✓ scoring.py - Test score: {test_result['score']}")
except Exception as e:
    print(f"✗ scoring.py: {e}")

try:
    from app.drafting import generate_drafts
    drafts = generate_drafts("Test post content", ["test_tag"], "Test rationale")
    print(f"✓ drafting.py - Generated {len(drafts)} drafts")
except Exception as e:
    print(f"✗ drafting.py: {e}")

print()

# Test configuration
print("Testing configuration...")
try:
    targets = Config.load_targets()
    print(f"✓ Loaded {len(targets)} targets from targets.json")

    llm_config = Config.get_llm_config()
    print(f"✓ LLM Provider: {llm_config['provider']}")
    print(f"  Enabled: {llm_config['enabled']}")
except Exception as e:
    print(f"✗ Configuration: {e}")

print()

# Test file structure
print("Checking file structure...")
required_files = [
    "app/config.py",
    "app/storage.py",
    "app/collector.py",
    "app/scoring.py",
    "app/drafting.py",
    "app/ui.py",
    "data/targets.json",
    "scripts/run_collector.py",
    "requirements.txt",
    ".env.example"
]

base_dir = Path(__file__).parent
for file_path in required_files:
    full_path = base_dir / file_path
    if full_path.exists():
        print(f"✓ {file_path}")
    else:
        print(f"✗ Missing: {file_path}")

print()

# Test directories
print("Checking directories...")
required_dirs = [
    "data",
    "data/screenshots",
    "data/browser_profile",
    "app",
    "scripts"
]

for dir_path in required_dirs:
    full_path = base_dir / dir_path
    if full_path.exists() and full_path.is_dir():
        print(f"✓ {dir_path}/")
    else:
        print(f"✗ Missing directory: {dir_path}/")

print()
print("=" * 60)
print("Setup test complete!")
print("=" * 60)
print()
print("If all tests passed, you're ready to run:")
print("  streamlit run app/ui.py")
print()
print("Or on Windows, double-click:")
print("  START_DASHBOARD.bat")
print()
