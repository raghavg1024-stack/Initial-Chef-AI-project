from unittest.mock import patch
from ai_assistance import chef_ai

def test_chef_ai_empty_question():
    with patch("ollama.chat") as mock_chat:
        result = chef_ai("")
        assert result == "Please ask a cooking question."
        mock_chat.assert_not_called()

def test_chef_ai_whitespace_question():
    with patch("ollama.chat") as mock_chat:
        result = chef_ai("   ")
        assert result == "Please ask a cooking question."
        mock_chat.assert_not_called()

def test_chef_ai_valid_question():
    mock_response = {
        'message': {
            'content': 'Here is a quick pasta recipe!'
        }
    }
    with patch("ollama.chat", return_value=mock_response) as mock_chat:
        result = chef_ai("How do I make pasta?")
        assert result == "Here is a quick pasta recipe!"
        mock_chat.assert_called_once()
