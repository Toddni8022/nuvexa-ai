import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')

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
