# Database — `database.py`

The `NuvexaDB` class wraps an SQLite database that persists user data, conversation history, shopping carts, and order history.

---

## Schema

### `users`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `INTEGER PK` | Auto-increment |
| `name` | `TEXT` | Unique display name |
| `avatar_style` | `TEXT` | Default: `Stylized Futuristic Human` |
| `created_at` | `TIMESTAMP` | Auto-set |

### `conversations`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `INTEGER PK` | Auto-increment |
| `user_id` | `INTEGER FK` | References `users.id` |
| `mode` | `TEXT` | `assistant \| shopping \| therapist \| builder` |
| `message` | `TEXT` | Message content |
| `role` | `TEXT` | `user \| assistant` |
| `timestamp` | `TIMESTAMP` | Auto-set |

Indexed on `(user_id, mode, timestamp)` for fast history lookups.

### `cart`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `INTEGER PK` | Auto-increment |
| `user_id` | `INTEGER FK` | References `users.id` |
| `product_name` | `TEXT` | — |
| `product_price` | `REAL` | — |
| `product_image` | `TEXT` | Emoji or URL |
| `product_description` | `TEXT` | — |
| `quantity` | `INTEGER` | Default: 1 |
| `added_at` | `TIMESTAMP` | Auto-set |

Adding the same product increments its `quantity` rather than inserting a duplicate row.

### `orders`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `INTEGER PK` | Auto-increment |
| `user_id` | `INTEGER FK` | References `users.id` |
| `items` | `TEXT` | JSON array of `{name, price, qty}` |
| `total_amount` | `REAL` | — |
| `status` | `TEXT` | Default: `completed` |
| `created_at` | `TIMESTAMP` | Auto-set |

---

## Class: `NuvexaDB`

### Constructor

```python
NuvexaDB()
```

Opens (or creates) the SQLite database file defined by `config.DB_NAME` and runs `CREATE TABLE IF NOT EXISTS` for all tables.

---

### Key Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `get_or_create_user(name)` | `int` | Returns existing user ID or creates a new user |
| `save_message(user_id, mode, message, role)` | `bool` | Saves a conversation message |
| `get_conversation_history(user_id, mode, limit)` | `List[Tuple]` | Returns `[(role, message), ...]` ordered chronologically |
| `add_to_cart(user_id, name, price, ...)` | `int \| None` | Adds item or increments quantity; returns cart row ID |
| `get_cart_items(user_id)` | `List[Tuple]` | Returns `(id, name, price, image, desc, qty)` tuples |
| `update_cart_quantity(cart_id, qty)` | `bool` | Updates quantity; calls `remove_from_cart` if qty < 1 |
| `remove_from_cart(cart_id)` | `bool` | Deletes a cart row |
| `clear_cart(user_id)` | `bool` | Deletes all cart rows for user |
| `create_order(user_id, items, total)` | `int \| None` | Saves order; returns order ID |
| `get_user_orders(user_id, limit)` | `List[Tuple]` | Returns recent orders |
| `update_avatar_style(user_id, style)` | `bool` | Updates avatar preference |
| `get_avatar_style(user_id)` | `str` | Returns current avatar style |

---

## Thread Safety

The connection is opened with `check_same_thread=False`, which is safe for Streamlit's single-threaded execution model. All writes go through the `get_cursor()` context manager which commits on success and rolls back on error.
