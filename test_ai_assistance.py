from unittest.mock import patch
import pytest
from ai_assistance import chef_ai

def test_chef_ai_caching():
    mock_response = {'message': {'content': 'Here is a delicious recipe!'}}

    with patch('ollama.chat', return_value=mock_response) as mock_chat:
        # First call should invoke ollama.chat
        res1 = chef_ai("How to boil eggs?")
        assert res1 == 'Here is a delicious recipe!'
        assert mock_chat.call_count == 1

        # Second call with identical argument should hit streamlit cache
        res2 = chef_ai("How to boil eggs?")
        assert res2 == 'Here is a delicious recipe!'
        assert mock_chat.call_count == 1  # call_count remains 1 due to @st.cache_data
