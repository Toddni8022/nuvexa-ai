from assistant import NuvexaAssistant
from database import NuvexaDB
from shopping import ShoppingEngine


def test_assistant_works_without_api_key():
    assistant = NuvexaAssistant(api_key="")
    assert assistant.client is None
    assert "not configured" in assistant.chat("hello").lower()


def test_unknown_product_query_returns_no_false_matches():
    engine = ShoppingEngine()
    assert engine.search_products("industrial fiber optic tester") == []
    assert engine.search_products("noise cancelling headphones")


def test_cart_and_checkout_data_round_trip(tmp_path):
    db = NuvexaDB(str(tmp_path / "nuvexa.db"))
    try:
        user_id = db.get_or_create_user("Todd")
        item_id = db.add_to_cart(user_id, "Test product", 19.99, quantity=2)
        assert item_id is not None
        items = db.get_cart_items(user_id)
        assert items[0][5] == 2
        order_id = db.create_order(user_id, [{"name": "Test product", "qty": 2}], 39.98)
        assert order_id is not None
    finally:
        db.close()
