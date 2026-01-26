from openai import OpenAI
from typing import Optional, List, Tuple
from config import OPENAI_API_KEY, MODES
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NuvexaAssistant:
    """AI Assistant with multiple operational modes."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the assistant with OpenAI API key."""
        # Get API key from parameter or config
        raw_key = api_key or OPENAI_API_KEY
        
        # Clean and validate the key
        if raw_key:
            self.api_key = str(raw_key).strip()
        else:
            self.api_key = None
        
        # Check if key is valid
        if not self.api_key or self.api_key == 'your-openai-api-key-here' or len(self.api_key) < 10:
            logger.warning(f"OpenAI API key not configured properly. Key length: {len(self.api_key) if self.api_key else 0}")
            logger.warning(f"Key value (first 20 chars): {self.api_key[:20] if self.api_key else 'None'}")
            self.client = None
        else:
            try:
                # Initialize client - this doesn't make an API call, just creates the client object
                self.client = OpenAI(api_key=self.api_key)
                logger.info(f"OpenAI client initialized successfully. Key starts with: {self.api_key[:10]}...")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {str(e)}")
                self.client = None
        self.current_mode = 'assistant'
    
    def set_mode(self, mode: str) -> bool:
        """Set the current operational mode."""
        if mode in MODES:
            self.current_mode = mode
            logger.info(f"Mode switched to: {mode}")
            return True
        logger.warning(f"Invalid mode attempted: {mode}")
        return False
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the current mode."""
        return MODES[self.current_mode]['system_prompt']
    
    def chat(self, user_message: str, conversation_history: Optional[List[Tuple[str, str]]] = None) -> str:
        """Generate a chat response using OpenAI API."""
        if not self.client:
            return "Error: OpenAI API key not configured. Please check your .env file."
        
        if not user_message or not user_message.strip():
            return "Please provide a message."
        
        try:
            messages = [{"role": "system", "content": self.get_system_prompt()}]
            
            if conversation_history:
                for role, content in conversation_history:
                    if role in ["user", "assistant"] and content:
                        messages.append({"role": role, "content": content})
            
            messages.append({"role": "user", "content": user_message.strip()})
            
            # Try models in order of preference
            models = ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]
            response = None
            last_error = None
            
            for model in models:
                try:
                    response = self.client.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=0.7,
                        max_tokens=800
                    )
                    logger.info(f"Successfully used model: {model}")
                    break
                except Exception as e:
                    last_error = e
                    error_str = str(e).lower()
                    # Only try next model if it's a model-specific error
                    if "model" not in error_str and "not found" not in error_str and "does not exist" not in error_str:
                        # This is likely an auth/quota issue, don't try other models
                        raise
                    logger.warning(f"Model {model} failed: {str(e)}, trying next...")
                    continue
            
            if not response:
                if last_error:
                    raise last_error
                else:
                    raise Exception("No models available")
            
            if response and response.choices and len(response.choices) > 0:
                return response.choices[0].message.content
            else:
                return "Error: Empty response from API. Please try again."
                
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            error_str = str(e)
            error_msg = error_str.lower()
            
            # Show the actual error message from OpenAI for debugging
            full_error = f"Error: {error_str}"
            
            # More specific error messages
            if "api key" in error_msg or "authentication" in error_msg or "invalid_api_key" in error_msg or "incorrect api key" in error_msg:
                return f"{full_error}\n\nYour API key format looks correct, but OpenAI rejected it. Please:\n1. Check if the key is still valid at https://platform.openai.com/api-keys\n2. Make sure there are no extra spaces in your .env file\n3. Try generating a new API key if this one was revoked"
            elif "rate limit" in error_msg or "rate_limit_exceeded" in error_msg:
                return "Error: Rate limit exceeded. Please wait a moment and try again."
            elif "insufficient_quota" in error_msg or "quota" in error_msg or "billing" in error_msg:
                return "Error: Insufficient API quota or billing issue. Please check your OpenAI account billing at https://platform.openai.com/account/billing"
            elif "connection" in error_msg or "timeout" in error_msg or "network" in error_msg:
                return f"Error: Connection issue. Please check your internet connection and try again.\n\nDetails: {error_str[:200]}"
            else:
                # Return the full error for debugging
                return f"{full_error}\n\nIf this persists, check:\n- Your API key is valid at https://platform.openai.com/api-keys\n- You have available credits/quota\n- Your internet connection is working"
    
    def analyze_shopping_intent(self, message: str) -> bool:
        """Analyze if the message contains shopping intent."""
        if not message:
            return False
        
        shopping_keywords = [
            'buy', 'purchase', 'shop', 'find', 'look for', 'need', 'want', 
            'get me', 'search for', 'looking for', 'shopping', 'order'
        ]
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in shopping_keywords)
    
    def extract_product_query(self, message: str) -> str:
        """Extract product search query from user message."""
        if not message:
            return ""
        
        shopping_keywords = [
            'buy', 'purchase', 'shop for', 'find', 'look for', 'need', 
            'want', 'get me', 'search for', 'looking for'
        ]
        message_lower = message.lower()
        
        for keyword in shopping_keywords:
            if keyword in message_lower:
                parts = message_lower.split(keyword, 1)
                if len(parts) > 1:
                    query = parts[1].strip()
                    # Clean up common words
                    for word in ['some', 'a', 'an', 'the']:
                        query = query.replace(word, '').strip()
                    return query if query else message
        
        return message
