"""Tests for the NuvexaDB database class."""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestGetOrCreateUser:
    def test_creates_new_user(self, temp_db):
        user_id = temp_db.get_or_create_user("Alice")
        assert isinstance(user_id, int)
        assert user_id > 0

    def test_returns_existing_user(self, temp_db):
        id1 = temp_db.get_or_create_user("Bob")
        id2 = temp_db.get_or_create_user("Bob")
        assert id1 == id2

    def test_creates_distinct_users(self, temp_db):
        id1 = temp_db.get_or_create_user("Carol")
        id2 = temp_db.get_or_create_user("Dave")
        assert id1 != id2

    def test_empty_name_defaults_to_user(self, temp_db):
        user_id = temp_db.get_or_create_user("")
        assert isinstance(user_id, int)


class TestSaveAndGetMessages:
    def test_save_and_retrieve_message(self, temp_db):
        user_id = temp_db.get_or_create_user("TestUser")
        result = temp_db.save_message(user_id, "assistant", "Hello world", "user")
        assert result is True

        history = temp_db.get_conversation_history(user_id, "assistant")
        assert len(history) == 1
        assert history[0] == ("user", "Hello world")

    def test_save_invalid_role_returns_false(self, temp_db):
        user_id = temp_db.get_or_create_user("TestUser2")
        result = temp_db.save_message(user_id, "assistant", "msg", "admin")
        assert result is False

    def test_save_empty_message_returns_false(self, temp_db):
        user_id = temp_db.get_or_create_user("TestUser3")
        result = temp_db.save_message(user_id, "assistant", "", "user")
        assert result is False

    def test_history_respects_mode(self, temp_db):
        user_id = temp_db.get_or_create_user("ModeUser")
        temp_db.save_message(user_id, "shopping", "buy shoes", "user")
        temp_db.save_message(user_id, "assistant", "hello", "user")

        shopping_history = temp_db.get_conversation_history(user_id, "shopping")
        assistant_history = temp_db.get_conversation_history(user_id, "assistant")

        assert len(shopping_history) == 1
        assert len(assistant_history) == 1


class TestCart:
    def test_add_to_cart(self, temp_db):
        user_id = temp_db.get_or_create_user("CartUser")
        cart_id = temp_db.add_to_cart(user_id, "Laptop", 999.99)
        assert cart_id is not None

    def test_add_duplicate_increases_quantity(self, temp_db):
        user_id = temp_db.get_or_create_user("CartUser2")
        temp_db.add_to_cart(user_id, "Phone", 299.99)
        temp_db.add_to_cart(user_id, "Phone", 299.99)

        items = temp_db.get_cart_items(user_id)
        assert len(items) == 1
        # quantity should be 2
        assert items[0][5] == 2

    def test_remove_from_cart(self, temp_db):
        user_id = temp_db.get_or_create_user("CartUser3")
        cart_id = temp_db.add_to_cart(user_id, "Tablet", 499.99)
        assert cart_id is not None

        result = temp_db.remove_from_cart(cart_id)
        assert result is True

        items = temp_db.get_cart_items(user_id)
        assert len(items) == 0

    def test_clear_cart(self, temp_db):
        user_id = temp_db.get_or_create_user("CartUser4")
        temp_db.add_to_cart(user_id, "Item1", 10.00)
        temp_db.add_to_cart(user_id, "Item2", 20.00)

        result = temp_db.clear_cart(user_id)
        assert result is True

        items = temp_db.get_cart_items(user_id)
        assert len(items) == 0

    def test_update_cart_quantity(self, temp_db):
        user_id = temp_db.get_or_create_user("CartUser5")
        cart_id = temp_db.add_to_cart(user_id, "Headphones", 199.99)
        assert cart_id is not None

        result = temp_db.update_cart_quantity(cart_id, 3)
        assert result is True

        items = temp_db.get_cart_items(user_id)
        assert items[0][5] == 3

    def test_add_invalid_price_returns_none(self, temp_db):
        user_id = temp_db.get_or_create_user("CartUser6")
        result = temp_db.add_to_cart(user_id, "BadItem", -1.00)
        assert result is None


class TestOrders:
    def test_create_order(self, temp_db):
        user_id = temp_db.get_or_create_user("OrderUser")
        items = [{"name": "Laptop", "price": 999.99, "qty": 1}]
        order_id = temp_db.create_order(user_id, items, 999.99)
        assert order_id is not None

    def test_get_user_orders(self, temp_db):
        user_id = temp_db.get_or_create_user("OrderUser2")
        items = [{"name": "Phone", "price": 299.99, "qty": 2}]
        temp_db.create_order(user_id, items, 599.98)

        orders = temp_db.get_user_orders(user_id)
        assert len(orders) == 1
        assert orders[0][2] == 599.98

    def test_create_order_empty_items_returns_none(self, temp_db):
        user_id = temp_db.get_or_create_user("OrderUser3")
        result = temp_db.create_order(user_id, [], 0.00)
        assert result is None


class TestAvatarStyle:
    def test_get_default_avatar_style(self, temp_db):
        user_id = temp_db.get_or_create_user("AvatarUser")
        style = temp_db.get_avatar_style(user_id)
        assert style == "Stylized Futuristic Human"

    def test_update_avatar_style(self, temp_db):
        user_id = temp_db.get_or_create_user("AvatarUser2")
        result = temp_db.update_avatar_style(user_id, "Anime Style")
        assert result is True
        assert temp_db.get_avatar_style(user_id) == "Anime Style"

    def test_update_invalid_avatar_style_returns_false(self, temp_db):
        user_id = temp_db.get_or_create_user("AvatarUser3")
        result = temp_db.update_avatar_style(user_id, "Invisible Style")
        assert result is False
