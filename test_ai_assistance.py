from unittest.mock import patch
import pytest
from ai_assistance import chef_ai

def test_chef_ai_empty_question():
    # Empty query should return prompt immediately without calling ollama
    with patch("ollama.chat") as mock_chat:
        result = chef_ai("")
        assert result == "Please enter a valid cooking question."
        mock_chat.assert_not_called()

def test_chef_ai_whitespace_question():
    # Whitespace query should return prompt immediately without calling ollama
    with patch("ollama.chat") as mock_chat:
        result = chef_ai("   ")
        assert result == "Please enter a valid cooking question."
        mock_chat.assert_not_called()

def test_chef_ai_valid_question():
    # Clear cache to ensure fresh call during test
    chef_ai.clear()
    with patch("ollama.chat") as mock_chat:
        mock_chat.return_value = {
            'message': {
                'content': 'Preheat oven to 350F.'
            }
        }
        result = chef_ai("How to bake cookies?")
        assert result == "Preheat oven to 350F."
        mock_chat.assert_called_once()
