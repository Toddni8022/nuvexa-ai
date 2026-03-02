# System Architecture

## Overview

NUVEXA is a single-page Streamlit web application. All components run in the same Python process; state is persisted in SQLite and held in Streamlit's `session_state` during a browser session.

```
┌─────────────────────────────────────────────┐
│                   Browser                   │
│         http://localhost:8501               │
└────────────────────┬────────────────────────┘
                     │ HTTP (Streamlit WebSocket)
┌────────────────────▼────────────────────────┐
│               app.py  (UI layer)            │
│  • Streamlit widgets & layout               │
│  • Session state management                 │
│  • Mode switching                           │
└──────┬─────────────┬──────────────┬─────────┘
       │             │              │
┌──────▼──────┐ ┌────▼──────┐ ┌───▼────────┐
│ assistant.py│ │database.py│ │shopping.py │
│ NuvexaAssis-│ │ NuvexaDB  │ │ Shopping-  │
│ tant        │ │ SQLite    │ │ Engine     │
└──────┬──────┘ └───────────┘ └────────────┘
       │
┌──────▼──────┐
│  OpenAI API │
│  (external) │
└─────────────┘
```

---

## Component Responsibilities

### `app.py` — UI Layer

* Defines the Streamlit page layout (header, sidebar, main chat, product panel)
* Manages `st.session_state` for the lifetime of a browser session
* Routes user input to `NuvexaAssistant.chat()` and `ShoppingEngine.search_products()`
* Reads/writes conversation and cart data via `NuvexaDB`

### `assistant.py` — AI Layer

* Wraps the OpenAI Chat Completions API
* Selects the appropriate system prompt from `config.MODES`
* Implements shopping-intent detection and product query extraction
* Handles model fallback (`gpt-4o` → `gpt-4` → `gpt-3.5-turbo`) and error surfacing

### `database.py` — Persistence Layer

* Manages four SQLite tables: `users`, `conversations`, `cart`, `orders`
* Provides a context-manager cursor with automatic commit/rollback

### `shopping.py` — Shopping Layer

* Holds a static product catalogue with six categories
* Multi-strategy keyword search with random fallback

### `config.py` — Configuration

* Loads `OPENAI_API_KEY` from `.env` (three fallback strategies for encoding issues)
* Defines `MODES`, `AVATAR_STYLES`, `APP_NAME`, `DB_NAME`, etc.

---

## Data Flow — Chat Message

```
User types message
       │
       ▼
app.py checks shopping intent (assistant.analyze_shopping_intent)
       │
       ├─ Yes → shopping_engine.search_products(query)
       │         → st.session_state.search_results
       │
       └─ No  → (skipped)
       │
       ▼
assistant.chat(message, history)
       │
       ▼
OpenAI Chat Completions API
       │
       ▼
Response saved to SQLite + session_state.messages
       │
       ▼
st.rerun() → UI re-renders with new message
```

---

## State Management

All runtime state lives in `st.session_state`:

| Key | Type | Description |
|-----|------|-------------|
| `db` | `NuvexaDB` | Shared DB instance |
| `user_id` | `int` | Current user's DB ID |
| `ai_assistant` | `NuvexaAssistant` | AI client |
| `shopping_engine` | `ShoppingEngine` | Product search |
| `current_mode` | `str` | Active mode key |
| `messages` | `list` | In-memory chat history |
| `search_results` | `list` | Last product search results |

Conversation history is additionally persisted in SQLite so it survives page refreshes.
