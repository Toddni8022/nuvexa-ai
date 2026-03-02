# API Reference

NUVEXA has no external HTTP API — it is a Streamlit application. This document describes the public Python interfaces exposed by each module.

---

## `assistant.NuvexaAssistant`

```python
class NuvexaAssistant:
    def __init__(self, api_key: Optional[str] = None) -> None: ...
    def set_mode(self, mode: str) -> bool: ...
    def get_system_prompt(self) -> str: ...
    def chat(
        self,
        user_message: str,
        conversation_history: Optional[List[Tuple[str, str]]] = None,
    ) -> str: ...
    def analyze_shopping_intent(self, message: str) -> bool: ...
    def extract_product_query(self, message: str) -> str: ...
```

---

## `database.NuvexaDB`

```python
class NuvexaDB:
    def __init__(self) -> None: ...

    # Users
    def get_or_create_user(self, name: str = "User") -> int: ...
    def update_avatar_style(self, user_id: int, avatar_style: str) -> bool: ...
    def get_avatar_style(self, user_id: int) -> str: ...

    # Conversations
    def save_message(self, user_id: int, mode: str, message: str, role: str) -> bool: ...
    def get_conversation_history(
        self, user_id: int, mode: str, limit: int = 20
    ) -> List[Tuple[str, str]]: ...

    # Cart
    def add_to_cart(
        self,
        user_id: int,
        product_name: str,
        product_price: float,
        product_image: str = "",
        product_description: str = "",
        quantity: int = 1,
    ) -> Optional[int]: ...
    def get_cart_items(self, user_id: int) -> List[Tuple]: ...
    def update_cart_quantity(self, cart_id: int, quantity: int) -> bool: ...
    def remove_from_cart(self, cart_id: int) -> bool: ...
    def clear_cart(self, user_id: int) -> bool: ...

    # Orders
    def create_order(
        self, user_id: int, items: List[Dict[str, Any]], total_amount: float
    ) -> Optional[int]: ...
    def get_user_orders(self, user_id: int, limit: int = 10) -> List[Tuple]: ...
```

---

## `shopping.ShoppingEngine`

```python
class ShoppingEngine:
    def __init__(self) -> None: ...
    def search_products(self, query: str) -> List[Dict[str, Any]]: ...
    def get_product_recommendations(self, category: str) -> List[Dict[str, Any]]: ...
```

**Product dict schema:**

```python
{
    "name": str,         # Display name
    "price": float,      # USD
    "image": str,        # Emoji
    "description": str,  # Short description
    "rating": float,     # 0–5 stars
    "source": str,       # Retailer
}
```

---

## `config` module constants

| Name | Type | Description |
|------|------|-------------|
| `OPENAI_API_KEY` | `str` | Loaded from `.env` |
| `APP_NAME` | `str` | `"NUVEXA"` |
| `APP_VERSION` | `str` | `"1.0.0"` |
| `APP_TAGLINE` | `str` | App tagline string |
| `MODES` | `dict` | Mode definitions (name, icon, description, system_prompt) |
| `AVATAR_STYLES` | `list[str]` | Available avatar style names |
| `DB_NAME` | `str` | SQLite database filename |
