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
            response = openai.chat.completions.create(model="gpt-4", messages=messages, temperature=0.7, max_tokens=800)
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}. Please check your API key."
    
    def analyze_shopping_intent(self, message):
        shopping_keywords = ['buy', 'purchase', 'shop', 'find', 'look for', 'need', 'want', 'get me']
        message_lower = message.lower()
        for keyword in shopping_keywords:
            if keyword in message_lower:
                return True
        return False
    
    def extract_product_query(self, message):
        shopping_keywords = ['buy', 'purchase', 'shop for', 'find', 'look for', 'need', 'want', 'get me']
        message_lower = message.lower()
        for keyword in shopping_keywords:
            if keyword in message_lower:
                parts = message_lower.split(keyword)
                if len(parts) > 1:
                    query = parts[1].strip()
                    query = query.replace('some', '').replace('a', '').replace('an', '').strip()
                    return query
        return message
