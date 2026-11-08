from unittest.mock import patch
import pytest
import ai_assistance

def test_chef_ai_empty_question():
    client = ai_assistance.get_ollama_client()
    with patch.object(client, "chat") as mock_chat:
        res1 = ai_assistance.chef_ai("")
        res2 = ai_assistance.chef_ai("   ")
        assert res1 == ""
        assert res2 == ""
        mock_chat.assert_not_called()

def test_chef_ai_valid_question_and_caching():
    client = ai_assistance.get_ollama_client()
    with patch.object(client, "chat") as mock_chat:
        mock_chat.return_value = {'message': {'content': 'Boil water and add pasta.'}}

        # Clear Streamlit cache for test isolation
        ai_assistance.chef_ai.clear()

        # First call should invoke client.chat
        res1 = ai_assistance.chef_ai("How to boil pasta?")
        assert res1 == 'Boil water and add pasta.'
        assert mock_chat.call_count == 1

        # Second call with identical input should be served from cache
        res2 = ai_assistance.chef_ai("How to boil pasta?")
        assert res2 == 'Boil water and add pasta.'
        # Call count remains 1 because cached output is returned without calling client.chat
        assert mock_chat.call_count == 1

def test_chef_ai_cache_normalization():
    client = ai_assistance.get_ollama_client()
    with patch.object(client, "chat") as mock_chat:
        mock_chat.return_value = {'message': {'content': 'Simmer for 20 minutes.'}}

        # Clear Streamlit cache for test isolation
        ai_assistance.chef_ai.clear()

        # Initial call
        res1 = ai_assistance.chef_ai("How to make tomato soup?")
        assert res1 == 'Simmer for 20 minutes.'
        assert mock_chat.call_count == 1

        # Case variations and extra spacing should hit the cache instead of calling Ollama
        res2 = ai_assistance.chef_ai("  how TO make tomato soup?  ")
        assert res2 == 'Simmer for 20 minutes.'
        assert mock_chat.call_count == 1

        res3 = ai_assistance.chef_ai("HOW  TO   MAKE   TOMATO   SOUP?")
        assert res3 == 'Simmer for 20 minutes.'
        assert mock_chat.call_count == 1
