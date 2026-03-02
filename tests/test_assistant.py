"""Tests for the NuvexaAssistant class."""

from unittest.mock import MagicMock, patch
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assistant import NuvexaAssistant


class TestNuvexaAssistantInit:
    def test_init_without_key_sets_client_none(self):
        assistant = NuvexaAssistant(api_key="your-openai-api-key-here")
        assert assistant.client is None

    def test_init_with_empty_key_sets_client_none(self):
        assistant = NuvexaAssistant(api_key="")
        assert assistant.client is None

    def test_init_sets_default_mode(self):
        assistant = NuvexaAssistant(api_key="")
        assert assistant.current_mode == "assistant"

    def test_init_with_short_key_sets_client_none(self):
        assistant = NuvexaAssistant(api_key="short")
        assert assistant.client is None


class TestSetMode:
    def setup_method(self):
        self.assistant = NuvexaAssistant(api_key="")

    def test_set_valid_mode(self):
        result = self.assistant.set_mode("shopping")
        assert result is True
        assert self.assistant.current_mode == "shopping"

    def test_set_all_valid_modes(self):
        for mode in ("assistant", "shopping", "therapist", "builder"):
            assert self.assistant.set_mode(mode) is True

    def test_set_invalid_mode_returns_false(self):
        result = self.assistant.set_mode("unknown_mode")
        assert result is False
        # Mode should not have changed
        assert self.assistant.current_mode == "assistant"


class TestGetSystemPrompt:
    def setup_method(self):
        self.assistant = NuvexaAssistant(api_key="")

    def test_returns_string(self):
        prompt = self.assistant.get_system_prompt()
        assert isinstance(prompt, str)
        assert len(prompt) > 0

    def test_prompt_changes_with_mode(self):
        prompt_assistant = self.assistant.get_system_prompt()
        self.assistant.set_mode("shopping")
        prompt_shopping = self.assistant.get_system_prompt()
        assert prompt_assistant != prompt_shopping


class TestChat:
    def setup_method(self):
        self.assistant = NuvexaAssistant(api_key="")

    def test_chat_without_client_returns_error(self):
        response = self.assistant.chat("Hello")
        assert "Error" in response

    def test_chat_with_empty_message_returns_message(self):
        response = self.assistant.chat("")
        assert isinstance(response, str)
        assert len(response) > 0

    def test_chat_with_mock_client(self):
        self.assistant.client = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "Hello, I'm NUVEXA!"
        self.assistant.client.chat.completions.create.return_value = MagicMock(
            choices=[mock_choice]
        )

        response = self.assistant.chat("Hello")
        assert response == "Hello, I'm NUVEXA!"

    def test_chat_with_conversation_history(self):
        self.assistant.client = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "I remember!"
        self.assistant.client.chat.completions.create.return_value = MagicMock(
            choices=[mock_choice]
        )

        history = [("user", "Previous message"), ("assistant", "Previous reply")]
        response = self.assistant.chat("New message", history)
        assert response == "I remember!"


class TestShoppingIntentAnalysis:
    def setup_method(self):
        self.assistant = NuvexaAssistant(api_key="")

    def test_buy_keyword_detected(self):
        assert self.assistant.analyze_shopping_intent("I want to buy headphones") is True

    def test_find_keyword_detected(self):
        assert self.assistant.analyze_shopping_intent("Find me a laptop") is True

    def test_non_shopping_message_returns_false(self):
        assert self.assistant.analyze_shopping_intent("What is the weather today?") is False

    def test_empty_message_returns_false(self):
        assert self.assistant.analyze_shopping_intent("") is False


class TestExtractProductQuery:
    def setup_method(self):
        self.assistant = NuvexaAssistant(api_key="")

    def test_extract_from_buy_statement_returns_string(self):
        query = self.assistant.extract_product_query("I want to buy headphones")
        assert isinstance(query, str)
        assert len(query) > 0

    def test_extract_from_find_statement_returns_string(self):
        query = self.assistant.extract_product_query("Find me a laptop")
        assert isinstance(query, str)
        assert len(query) > 0

    def test_extract_without_keyword_returns_original(self):
        msg = "wireless earbuds"
        query = self.assistant.extract_product_query(msg)
        assert query == msg

    def test_empty_message_returns_empty(self):
        query = self.assistant.extract_product_query("")
        assert query == ""
