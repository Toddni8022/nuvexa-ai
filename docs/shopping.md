# Shopping Module — `shopping.py`

The `ShoppingEngine` class provides a simulated product catalogue with keyword-based search and category recommendations.

---

## Class: `ShoppingEngine`

### Constructor

```python
ShoppingEngine()
```

Loads the built-in product catalogue and keyword-to-category mapping on initialisation.

---

### Methods

#### `search_products(query: str) → List[Dict[str, Any]]`

Search the catalogue for products matching the query.

```python
engine = ShoppingEngine()
results = engine.search_products("wireless headphones")
```

**Search strategy** (in order):

1. Direct category match (`"laptop"` → laptop category)
2. Keyword mapping (`"computer"` → laptop category)
3. Partial word matching on category names
4. Full-text search across product names and descriptions
5. Random recommendations (fallback when nothing matches)

Returns at most **10 unique products**.

Each product dict has the following keys:

| Key | Type | Description |
|-----|------|-------------|
| `name` | `str` | Product display name |
| `price` | `float` | Price in USD |
| `image` | `str` | Emoji icon |
| `description` | `str` | Short description |
| `rating` | `float` | Star rating (0–5) |
| `source` | `str` | Retailer name |

---

#### `get_product_recommendations(category: str) → List[Dict[str, Any]]`

Return all products in a specific category (exact lowercase match).

```python
results = engine.get_product_recommendations("laptop")
```

---

## Supported Categories

| Category | Products |
|----------|---------|
| `coconut water` | 4 products |
| `peptides` | 3 products |
| `laptop` | 4 products |
| `headphones` | 4 products |
| `phone` | 3 products |
| `tablet` | 2 products |

---

## Keyword Mapping

| Keyword | Category |
|---------|----------|
| `coconut`, `coco` | `coconut water` |
| `collagen`, `peptide`, `supplement` | `peptides` |
| `computer`, `notebook`, `macbook` | `laptop` |
| `headphone`, `earphone`, `earbud` | `headphones` |
| `smartphone`, `mobile` | `phone` |
| `ipad` | `tablet` |
