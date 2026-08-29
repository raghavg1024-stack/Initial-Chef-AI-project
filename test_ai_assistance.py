from unittest.mock import patch
from ai_assistance import chef_ai, SYSTEM_PROMPT


def test_system_prompt_constant():
    assert "You are a chef." in SYSTEM_PROMPT
    assert "rules:" in SYSTEM_PROMPT


@patch("ollama.chat")
def test_chef_ai(mock_ollama_chat):
    mock_ollama_chat.return_value = {
        'message': {
            'content': 'To boil an egg, place it in boiling water for 6-7 minutes.'
        }
    }

    # Clear Streamlit cache if needed for test isolation
    chef_ai.clear()

    res = chef_ai("How do I boil an egg?")
    assert res == 'To boil an egg, place it in boiling water for 6-7 minutes.'

    mock_ollama_chat.assert_called_once_with(
        model='mistral',
        messages=[
            {
                'role': 'system',
                'content': SYSTEM_PROMPT
            },
            {
                'role': 'user',
                'content': "How do I boil an egg?"
            }
        ]
    )


@patch("ollama.chat")
def test_chef_ai_caching(mock_ollama_chat):
    mock_ollama_chat.return_value = {
        'message': {
            'content': 'Cached response.'
        }
    }

    chef_ai.clear()

    res1 = chef_ai("How to bake a cake?")
    res2 = chef_ai("How to bake a cake?")

    assert res1 == 'Cached response.'
    assert res2 == 'Cached response.'
    # Ensure ollama.chat was only called ONCE despite two calls to chef_ai
    assert mock_ollama_chat.call_count == 1
