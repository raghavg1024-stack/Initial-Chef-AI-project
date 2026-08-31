from unittest.mock import patch
import pytest

@patch('ollama.chat')
def test_chef_ai(mock_ollama_chat):
    mock_ollama_chat.return_value = {
        'message': {
            'content': 'Preheat oven to 350°F.'
        }
    }
    from ai_assistance import chef_ai

    # First call - should invoke ollama.chat
    res1 = chef_ai("How to bake?")
    assert res1 == 'Preheat oven to 350°F.'
    assert mock_ollama_chat.call_count == 1

    # Second call with same argument - cached, should NOT invoke ollama.chat again
    res2 = chef_ai("How to bake?")
    assert res2 == 'Preheat oven to 350°F.'
    assert mock_ollama_chat.call_count == 1
