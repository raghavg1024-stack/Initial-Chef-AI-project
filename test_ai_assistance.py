from unittest.mock import patch
from ai_assistance import chef_ai

def test_chef_ai_empty_question():
    with patch("ollama.chat") as mock_chat:
        res = chef_ai("")
        assert res == "Please enter a valid cooking question."
        mock_chat.assert_not_called()

def test_chef_ai_whitespace_question():
    with patch("ollama.chat") as mock_chat:
        res = chef_ai("   ")
        assert res == "Please enter a valid cooking question."
        mock_chat.assert_not_called()

def test_chef_ai_valid_question():
    with patch("ollama.chat") as mock_chat:
        mock_chat.return_value = {
            'message': {'content': 'To make scrambled eggs, whisk eggs and cook over low heat.'}
        }
        res = chef_ai("How do I make scrambled eggs?")
        assert res == "To make scrambled eggs, whisk eggs and cook over low heat."
        mock_chat.assert_called_once()
