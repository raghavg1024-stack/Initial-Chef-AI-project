from unittest.mock import patch
import streamlit as st
from ai_assistance import chef_ai

def test_chef_ai_empty_question():
    """Test early return logic for empty or whitespace-only questions."""
    with patch("ollama.chat") as mock_chat:
        res1 = chef_ai("")
        res2 = chef_ai("   ")
        assert res1 == "Please enter a valid cooking question."
        assert res2 == "Please enter a valid cooking question."
        mock_chat.assert_not_called()

def test_chef_ai_caching_and_api_call():
    """Test that chef_ai caches results and only calls ollama.chat once for identical questions."""
    st.cache_data.clear()

    with patch("ollama.chat") as mock_chat:
        mock_chat.return_value = {
            'message': {
                'content': 'Preheat the oven to 375°F.'
            }
        }

        # First call should invoke ollama.chat
        res1 = chef_ai("How to bake cookies?")
        assert res1 == 'Preheat the oven to 375°F.'
        assert mock_chat.call_count == 1

        # Second call with the same question should hit Streamlit cache
        res2 = chef_ai("How to bake cookies?")
        assert res2 == 'Preheat the oven to 375°F.'
        assert mock_chat.call_count == 1
