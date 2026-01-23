"""
OpenAI API integration service.
Handles chat completions with context management.
"""
from openai import OpenAI
from app.config import get_settings
from typing import List, Dict

settings = get_settings()


class OpenAIService:
    """Service for interacting with OpenAI API."""

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.max_tokens = settings.openai_max_tokens

    def get_system_prompt(self, mode: str) -> str:
        """Get system prompt based on conversation mode."""
        prompts = {
            "assistant": """You are NUVEXA, a helpful and friendly AI assistant.
You provide clear, concise, and actionable advice. You're knowledgeable about a wide range of topics
and always aim to be helpful while keeping responses focused and practical.""",

            "shopping": """You are NUVEXA Shopping Assistant. Help users find products they're looking for.
When a user asks about a product, acknowledge their request and let them know you're searching for options.
Keep responses concise and friendly. If specific products are shown, help them compare features and make decisions."""
        }
        return prompts.get(mode, prompts["assistant"])

    def format_conversation_history(
        self,
        history: List[Dict],
        mode: str
    ) -> List[Dict[str, str]]:
        """Format conversation history for OpenAI API."""
        messages = [{"role": "system", "content": self.get_system_prompt(mode)}]

        # Add conversation history (limit to last 10 messages for context window)
        for msg in history[-10:]:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role in ["user", "assistant"] and content:
                messages.append({"role": role, "content": content})

        return messages

    async def get_chat_response(
        self,
        message: str,
        mode: str = "assistant",
        history: List[Dict] = None
    ) -> str:
        """
        Get chat completion from OpenAI.

        Args:
            message: User's message
            mode: Conversation mode (assistant/shopping)
            history: Previous conversation messages

        Returns:
            AI assistant's response
        """
        if history is None:
            history = []

        try:
            # Format messages with system prompt and history
            messages = self.format_conversation_history(history, mode)
            messages.append({"role": "user", "content": message})

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=0.7,
            )

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def extract_product_query(self, message: str) -> str:
        """
        Extract product search query from user message.
        Simple keyword extraction for shopping mode.
        """
        # Remove common words/phrases
        stopwords = [
            "find", "search", "looking for", "show me", "i want", "i need",
            "can you", "please", "help me", "get me", "buy"
        ]

        query = message.lower()
        for word in stopwords:
            query = query.replace(word, "")

        return query.strip()
