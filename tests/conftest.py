"""Test configuration and shared fixtures for the NUVEXA test suite."""

import pytest
import sys
import os

# Ensure root-level modules are importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Provide a temporary SQLite database for each test."""
    db_path = str(tmp_path / "test_nuvexa.db")
    monkeypatch.setenv("NUVEXA_DB_NAME", db_path)

    # Patch the DB_NAME used inside database.py
    import database as db_module
    monkeypatch.setattr(db_module, "DB_NAME", db_path)

    from database import NuvexaDB
    db = NuvexaDB()
    yield db
    db.conn.close()


@pytest.fixture
def shopping_engine():
    """Provide a ShoppingEngine instance."""
    from shopping import ShoppingEngine
    return ShoppingEngine()
