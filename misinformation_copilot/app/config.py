"""Configuration management for Misinformation Debunking Copilot"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent.resolve()
DATA_DIR = BASE_DIR / "data"
SCREENSHOTS_DIR = DATA_DIR / "screenshots"
BROWSER_PROFILE_DIR = DATA_DIR / "browser_profile"
DB_PATH = DATA_DIR / "posts.db"
TARGETS_PATH = DATA_DIR / "targets.json"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)
BROWSER_PROFILE_DIR.mkdir(exist_ok=True)


class Config:
    """Application configuration"""

    # LLM Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")  # mock, openai, anthropic, ollama
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")

    # OpenAI model settings
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

    # Anthropic model settings
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")

    # Collection settings (defaults)
    DEFAULT_SCROLL_PASSES = 3
    DEFAULT_SCROLL_DELAY = 2.0  # seconds
    DEFAULT_MAX_POSTS_PER_TARGET = 20
    DEFAULT_MAX_TARGETS_PER_RUN = 5

    # Browser settings
    BROWSER_HEADLESS = os.getenv("BROWSER_HEADLESS", "false").lower() == "true"
    BROWSER_TIMEOUT = 30000  # milliseconds

    # Scoring thresholds
    MISINFO_THRESHOLD_HIGH = 70
    MISINFO_THRESHOLD_MEDIUM = 40

    @staticmethod
    def load_targets() -> List[Dict[str, Any]]:
        """Load targets from targets.json"""
        if not TARGETS_PATH.exists():
            return []

        try:
            with open(TARGETS_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('targets', [])
        except Exception as e:
            print(f"Error loading targets: {e}")
            return []

    @staticmethod
    def save_targets(targets: List[Dict[str, Any]]) -> bool:
        """Save targets to targets.json"""
        try:
            with open(TARGETS_PATH, 'w', encoding='utf-8') as f:
                json.dump({'targets': targets}, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving targets: {e}")
            return False

    @staticmethod
    def get_llm_config() -> Dict[str, Any]:
        """Get LLM configuration based on provider"""
        provider = Config.LLM_PROVIDER.lower()

        if provider == "openai":
            return {
                "provider": "openai",
                "api_key": Config.OPENAI_API_KEY,
                "model": Config.OPENAI_MODEL,
                "enabled": bool(Config.OPENAI_API_KEY)
            }
        elif provider == "anthropic":
            return {
                "provider": "anthropic",
                "api_key": Config.ANTHROPIC_API_KEY,
                "model": Config.ANTHROPIC_MODEL,
                "enabled": bool(Config.ANTHROPIC_API_KEY)
            }
        elif provider == "ollama":
            return {
                "provider": "ollama",
                "url": Config.OLLAMA_URL,
                "model": Config.OLLAMA_MODEL,
                "enabled": True  # Ollama doesn't need API key
            }
        else:  # mock
            return {
                "provider": "mock",
                "enabled": True
            }


# Export commonly used paths
__all__ = [
    'Config',
    'BASE_DIR',
    'DATA_DIR',
    'SCREENSHOTS_DIR',
    'BROWSER_PROFILE_DIR',
    'DB_PATH',
    'TARGETS_PATH'
]
