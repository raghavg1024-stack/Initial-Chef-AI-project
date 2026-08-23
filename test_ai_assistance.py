from unittest.mock import patch
import pytest
import streamlit as st
from ai_assistance import chef_ai

def test_chef_ai():
    # Clear streamlit cache before testing
    st.cache_data.clear()

    mock_response = {
        'message': {
            'content': 'Boil water, add pasta, cook for 8 to 10 minutes.'
        }
    }

    with patch('ollama.chat', return_value=mock_response) as mock_chat:
        # First call should hit ollama.chat
        res1 = chef_ai("How to make pasta?")
        assert res1 == 'Boil water, add pasta, cook for 8 to 10 minutes.'
        assert mock_chat.call_count == 1

        # Second call with same parameter should use cache and not call ollama.chat again
        res2 = chef_ai("How to make pasta?")
        assert res2 == 'Boil water, add pasta, cook for 8 to 10 minutes.'
        assert mock_chat.call_count == 1
