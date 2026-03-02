# AI Assistant — `assistant.py`

The `NuvexaAssistant` class provides the AI backbone for NUVEXA, wrapping the OpenAI Chat Completions API and supporting multiple operational modes.

---

## Class: `NuvexaAssistant`

### Constructor

```python
NuvexaAssistant(api_key: Optional[str] = None)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | `str \| None` | OpenAI API key. Falls back to `config.OPENAI_API_KEY` when `None`. |

If no valid key is provided, `self.client` is set to `None` and all chat calls return a descriptive error string.

---

### Methods

#### `set_mode(mode: str) → bool`

Switch the assistant to a different operational mode.

```python
assistant.set_mode("shopping")  # → True
assistant.set_mode("invalid")   # → False
```

Valid modes: `assistant`, `shopping`, `therapist`, `builder`.

---

#### `get_system_prompt() → str`

Return the system prompt for the current mode (defined in `config.MODES`).

---

#### `chat(user_message, conversation_history=None) → str`

Send a message and receive a response from OpenAI.

```python
response = assistant.chat(
    "Find me a good laptop",
    conversation_history=[("user", "Hi"), ("assistant", "Hello!")]
)
```

Model preference order: `gpt-4o` → `gpt-4` → `gpt-3.5-turbo`.

---

#### `analyze_shopping_intent(message: str) → bool`

Return `True` if the message contains shopping-related keywords.

---

#### `extract_product_query(message: str) → str`

Strip shopping trigger words and return the product search term.

---

## Modes

| Key | Name | Description |
|-----|------|-------------|
| `assistant` | Assistant | General help and planning |
| `shopping` | Shopping | Product discovery and checkout |
| `therapist` | Therapist | Emotional support |
| `builder` | Builder | Project planning |

Mode system prompts are defined in `config.MODES[mode]['system_prompt']`.

---

## Error Handling

All errors from the OpenAI API are caught and returned as descriptive strings starting with `"Error:"`. The caller (Streamlit UI) displays them in the chat without crashing.
