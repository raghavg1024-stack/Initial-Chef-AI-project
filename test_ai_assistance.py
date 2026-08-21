from unittest.mock import patch
from ai_assistance import chef_ai

def test_chef_ai_empty_question():
    with patch("ollama.chat") as mock_chat:
        result = chef_ai("")
        assert result == "Please ask a cooking question."
        mock_chat.assert_not_called()

        result_whitespace = chef_ai("   ")
        assert result_whitespace == "Please ask a cooking question."
        mock_chat.assert_not_called()

def test_chef_ai_valid_question():
    with patch("ollama.chat") as mock_chat:
        mock_chat.return_value = {
            'message': {
                'content': 'To boil an egg, place it in boiling water for 6-7 minutes.'
            }
        }

        result = chef_ai("How to boil an egg?")
        assert result == 'To boil an egg, place it in boiling water for 6-7 minutes.'
        mock_chat.assert_called_once()

        # Verify call parameters
        args, kwargs = mock_chat.call_args
        assert kwargs['model'] == 'mistral'
        assert kwargs['messages'][1]['content'] == 'How to boil an egg?'

def test_chef_ai_caching():
    with patch("ollama.chat") as mock_chat:
        mock_chat.return_value = {
            'message': {
                'content': 'Salt adds flavor.'
            }
        }

        # First call with a unique question for caching test
        res1 = chef_ai("Why use salt?")
        # Second call with same question
        res2 = chef_ai("Why use salt?")

        assert res1 == 'Salt adds flavor.'
        assert res2 == 'Salt adds flavor.'
        # Streamlit caching ensures ollama.chat is only called once
        assert mock_chat.call_count == 1
