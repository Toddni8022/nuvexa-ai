import openai
from config import OPENAI_API_KEY, MODES

class NuvexaAssistant:
    def __init__(self, api_key=None):
        self.api_key = api_key or OPENAI_API_KEY
        openai.api_key = self.api_key
        self.current_mode = 'assistant'
    
    def set_mode(self, mode):
        if mode in MODES:
            self.current_mode = mode
            return True
        return False
    
    def get_system_prompt(self):
        return MODES[self.current_mode]['system_prompt']
    
    def chat(self, user_message, conversation_history=None):
        try:
            messages = [{"role": "system", "content": self.get_system_prompt()}]
            if conversation_history:
                for role, content in conversation_history:
                    messages.append({"role": role, "content": content})
            messages.append({"role": "user", "content": user_message})
            response = openai.chat.completions.create(model="gpt-4", messages=messages, temperature=0.7, max_tokens=500)
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}. Please check your API key."
    
    def analyze_shopping_intent(self, message):
        """Returns True if message contains shopping intent - VERY AGGRESSIVE"""
        # If in shopping mode, ALWAYS return True
        if self.current_mode == 'shopping':
            return True
        
        shopping_keywords = [
            'buy', 'purchase', 'shop', 'shopping', 'find', 'look for', 'looking for',
            'need', 'want', 'get', 'order', 'search', 'show me', 'recommend',
            'suggestions', 'best', 'cheapest', 'price', 'cost', 'affordable',
            'candlestick', 'chocolate', 'laptop', 'headphones', 'water', 'peptides'
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in shopping_keywords)
    
    def extract_product_query(self, message):
        """Extract what product the user wants"""
        message_lower = message.lower().strip()
        
        # Remove common filler words
        remove_words = ['find me', 'i need', 'i want', 'get me', 'show me', 'looking for', 
                       'a', 'an', 'the', 'some', 'please', 'can you']
        
        for word in remove_words:
            message_lower = message_lower.replace(word, '')
        
        # Extract key product terms
        product_keywords = {
            'candlestick': 'candlestick',
            'candle': 'candlestick',
            'chocolate': 'chocolate',
            'coconut water': 'coconut water',
            'water': 'coconut water',
            'laptop': 'laptop',
            'computer': 'laptop',
            'headphones': 'headphones',
            'headphone': 'headphones',
            'peptides': 'peptides',
            'collagen': 'peptides'
        }
        
        for keyword, product in product_keywords.items():
            if keyword in message_lower:
                return product
        
        return message_lower.strip()
