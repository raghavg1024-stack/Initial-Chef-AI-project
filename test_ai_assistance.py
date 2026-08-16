from unittest.mock import patch, MagicMock
import pytest
from ai_assistance import chef_ai, SYSTEM_PROMPT


def test_chef_ai_empty_input():
    # Calling with empty or whitespace string should return notice immediately without invoking ollama.chat
    with patch("ollama.chat") as mock_chat:
        res = chef_ai("")
        assert res == "Please enter a valid cooking question."
        mock_chat.assert_not_called()

        res_space = chef_ai("   ")
        assert res_space == "Please enter a valid cooking question."
        mock_chat.assert_not_called()


def test_chef_ai_valid_question():
    with patch("ollama.chat") as mock_chat:
        mock_chat.return_value = {
            'message': {'content': 'Boil water and add pasta.'}
        }
        res = chef_ai("How to make pasta?")
        assert res == 'Boil water and add pasta.'
        mock_chat.assert_called_once_with(
            model='mistral',
            messages=[
                SYSTEM_PROMPT,
                {'role': 'user', 'content': "How to make pasta?"}
            ]
        )
