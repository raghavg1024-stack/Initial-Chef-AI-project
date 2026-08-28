from unittest.mock import patch
import pytest
from ai_assistance import chef_ai


@patch("ollama.chat")
def test_chef_ai(mock_ollama_chat):
    mock_ollama_chat.return_value = {
        "message": {"content": "Here is a recipe for pasta."}
    }

    response = chef_ai("How to make pasta?")
    assert response == "Here is a recipe for pasta."
    mock_ollama_chat.assert_called_once()
