"""Tests for the ShoppingEngine class."""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shopping import ShoppingEngine


class TestSearchProducts:
    def test_search_returns_list(self, shopping_engine):
        results = shopping_engine.search_products("laptop")
        assert isinstance(results, list)

    def test_search_laptop(self, shopping_engine):
        results = shopping_engine.search_products("laptop")
        assert len(results) > 0

    def test_search_headphones(self, shopping_engine):
        results = shopping_engine.search_products("headphones")
        assert len(results) > 0

    def test_search_coconut_water(self, shopping_engine):
        results = shopping_engine.search_products("coconut water")
        assert len(results) > 0

    def test_search_by_keyword(self, shopping_engine):
        # "computer" should map to laptop category
        results = shopping_engine.search_products("computer")
        assert len(results) > 0

    def test_search_empty_query_returns_empty(self, shopping_engine):
        results = shopping_engine.search_products("")
        assert results == []

    def test_search_returns_at_most_10_results(self, shopping_engine):
        results = shopping_engine.search_products("laptop")
        assert len(results) <= 10

    def test_search_result_has_required_fields(self, shopping_engine):
        results = shopping_engine.search_products("headphones")
        for product in results:
            assert "name" in product
            assert "price" in product

    def test_search_no_duplicates(self, shopping_engine):
        results = shopping_engine.search_products("laptop")
        names = [r["name"] for r in results]
        assert len(names) == len(set(names))

    def test_search_unknown_query_returns_recommendations(self, shopping_engine):
        # Unknown queries fall back to random recommendations
        results = shopping_engine.search_products("xyzunknownproduct12345")
        assert isinstance(results, list)
        # Should still return something (random recommendations)
        assert len(results) > 0

    def test_search_keyword_mapping_collagen_to_peptides(self, shopping_engine):
        results = shopping_engine.search_products("collagen")
        assert len(results) > 0
        names = " ".join(r["name"].lower() for r in results)
        assert "collagen" in names or "peptide" in names


class TestGetProductRecommendations:
    def test_get_recommendations_for_valid_category(self, shopping_engine):
        results = shopping_engine.get_product_recommendations("laptop")
        assert len(results) > 0

    def test_get_recommendations_for_invalid_category(self, shopping_engine):
        results = shopping_engine.get_product_recommendations("nonexistent")
        assert results == []

    def test_get_recommendations_case_insensitive(self, shopping_engine):
        results = shopping_engine.get_product_recommendations("LAPTOP")
        assert len(results) > 0
