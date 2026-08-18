from unittest.mock import patch, MagicMock
from ai_assistance import chef_ai, SYSTEM_PROMPT

def test_chef_ai_calls_ollama():
    mock_response = {
        'message': {
            'content': 'Here is a quick pasta recipe!'
        }
    }
    with patch('ollama.chat', return_value=mock_response) as mock_chat:
        # Clear Streamlit cache before test run if necessary
        chef_ai.clear()

        result = chef_ai("How to make pasta?")

        assert result == 'Here is a quick pasta recipe!'
        mock_chat.assert_called_once_with(
            model='mistral',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': "How to make pasta?"}
            ]
        )

def test_chef_ai_caching():
    mock_response = {
        'message': {
            'content': 'Boil water for 10 minutes.'
        }
    }
    with patch('ollama.chat', return_value=mock_response) as mock_chat:
        chef_ai.clear()

        # First call should invoke ollama.chat
        res1 = chef_ai("How to boil water?")
        # Second call with the same parameter should hit Streamlit cache and NOT invoke ollama.chat again
        res2 = chef_ai("How to boil water?")

        assert res1 == 'Boil water for 10 minutes.'
        assert res2 == 'Boil water for 10 minutes.'
        assert mock_chat.call_count == 1
