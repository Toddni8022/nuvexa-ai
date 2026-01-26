import os
from dotenv import load_dotenv
from typing import Dict, Any
from pathlib import Path

# Get the directory where this config file is located
BASE_DIR = Path(__file__).resolve().parent

# Load .env file from the same directory as this script
env_path = BASE_DIR / '.env'

# Try multiple methods to load the API key
OPENAI_API_KEY = None

# Method 1: Try load_dotenv with explicit path
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Method 2: Try load_dotenv from current directory
if not OPENAI_API_KEY:
    load_dotenv(override=True)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Method 3: Read directly from file (most reliable fallback)
# This handles BOM and encoding issues
if not OPENAI_API_KEY or OPENAI_API_KEY == 'your-openai-api-key-here':
    if env_path.exists():
        try:
            # Use utf-8-sig to automatically strip BOM
            with open(env_path, 'r', encoding='utf-8-sig') as f:
                for line in f:
                    # Strip BOM and whitespace
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue
                    # Check if line contains OPENAI_API_KEY (handles BOM at start)
                    if 'OPENAI_API_KEY' in line and '=' in line:
                        # Split on = and handle BOM in key name
                        parts = line.split('=', 1)
                        if len(parts) == 2:
                            key = parts[0].strip().lstrip('\ufeff').strip()
                            if key == 'OPENAI_API_KEY':
                                OPENAI_API_KEY = parts[1].strip()
                                # Remove quotes if present
                                if OPENAI_API_KEY.startswith('"') and OPENAI_API_KEY.endswith('"'):
                                    OPENAI_API_KEY = OPENAI_API_KEY[1:-1]
                                elif OPENAI_API_KEY.startswith("'") and OPENAI_API_KEY.endswith("'"):
                                    OPENAI_API_KEY = OPENAI_API_KEY[1:-1]
                                break
        except Exception as e:
            # Last resort: try reading as bytes and decoding
            try:
                with open(env_path, 'rb') as f:
                    content = f.read().decode('utf-8-sig')
                    for line in content.splitlines():
                        line = line.strip()
                        if 'OPENAI_API_KEY' in line and '=' in line:
                            parts = line.split('=', 1)
                            if len(parts) == 2:
                                key = parts[0].strip().lstrip('\ufeff').strip()
                                if key == 'OPENAI_API_KEY':
                                    OPENAI_API_KEY = parts[1].strip()
                                    break
            except Exception:
                pass

# Final fallback
if not OPENAI_API_KEY or OPENAI_API_KEY == 'your-openai-api-key-here':
    OPENAI_API_KEY = 'your-openai-api-key-here'

APP_NAME = "NUVEXA"
APP_VERSION = "1.0.0"
APP_TAGLINE = "Your Living AI Assistant with Execution Power"

MODES = {
    'assistant': {
        'name': 'Assistant',
        'icon': '🤖',
        'description': 'General help, planning, and research',
        'system_prompt': 'You are NUVEXA, a helpful living AI assistant. You help users with tasks, planning, research, and provide actionable advice. You can help users shop, plan projects, and complete tasks. Be friendly, engaging, and proactive.'
    },
    'shopping': {
        'name': 'Shopping',
        'icon': '🛒',
        'description': 'Product search and purchase execution',
        'system_prompt': 'You are NUVEXA in Shopping Mode. Help users find products, compare options, and add items to their cart. Be detailed about product features, prices, and availability. Guide them through the purchase process seamlessly.'
    },
    'therapist': {
        'name': 'Therapist',
        'icon': '💭',
        'description': 'Emotional support and active listening',
        'system_prompt': 'You are NUVEXA in Therapist Mode. Listen actively, empathize deeply, and provide emotional support. Help users process their thoughts and feelings. Be warm, non-judgmental, and supportive. Ask thoughtful questions to help them explore their emotions.'
    },
    'builder': {
        'name': 'Builder',
        'icon': '🏗️',
        'description': 'Visual planning and project simulation',
        'system_prompt': 'You are NUVEXA in Builder Mode. Help users visualize and plan projects like building a PC, home renovation, or any assembly project. Break down complex projects into steps, recommend parts/materials, and create actionable plans with pricing.'
    }
}

AVATAR_STYLES = [
    'Stylized Futuristic Human',
    'Realistic Human',
    'Anime Style',
    'Cartoon Style',
    'Minimalist Icon'
]

DB_NAME = 'nuvexa.db'
