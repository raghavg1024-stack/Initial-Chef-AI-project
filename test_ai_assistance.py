from unittest.mock import patch
import pytest
from ai_assistance import chef_ai


def test_chef_ai_empty_question():
    with patch("ollama.chat") as mock_chat:
        result = chef_ai("")
        assert result == "Please ask a cooking question!"
        mock_chat.assert_not_called()


def test_chef_ai_whitespace_question():
    with patch("ollama.chat") as mock_chat:
        result = chef_ai("   \n\t  ")
        assert result == "Please ask a cooking question!"
        mock_chat.assert_not_called()


def test_chef_ai_valid_question():
    with patch("ollama.chat") as mock_chat:
        mock_chat.return_value = {"message": {"content": "Boil water for 10 minutes."}}
        result = chef_ai("How to boil an egg?")
        assert result == "Boil water for 10 minutes."
        mock_chat.assert_called_once()
        args, kwargs = mock_chat.call_args
        assert kwargs["model"] == "mistral"
        assert kwargs["messages"][-1]["content"] == "How to boil an egg?"
