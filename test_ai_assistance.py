from unittest.mock import patch
import pytest
import ai_assistance

def test_chef_ai_empty_question():
    with patch("ollama.chat") as mock_chat:
        res1 = ai_assistance.chef_ai("")
        res2 = ai_assistance.chef_ai("   ")
        assert res1 == ""
        assert res2 == ""
        mock_chat.assert_not_called()

def test_chef_ai_valid_question_and_caching():
    with patch("ollama.chat") as mock_chat:
        mock_chat.return_value = {'message': {'content': 'Boil water and add pasta.'}}

        # Clear Streamlit cache for test isolation
        ai_assistance.chef_ai.clear()

        # First call should invoke ollama.chat
        res1 = ai_assistance.chef_ai("How to boil pasta?")
        assert res1 == 'Boil water and add pasta.'
        assert mock_chat.call_count == 1

        # Check system prompt passed to ollama.chat
        _, kwargs = mock_chat.call_args
        assert kwargs['messages'][0]['content'] == ai_assistance.SYSTEM_PROMPT

        # Second call with identical input should be served from cache
        res2 = ai_assistance.chef_ai("How to boil pasta?")
        assert res2 == 'Boil water and add pasta.'
        # Call count remains 1 because cached output is returned without calling ollama.chat
        assert mock_chat.call_count == 1

def test_chef_ai_whitespace_normalization_cache_hit():
    with patch("ollama.chat") as mock_chat:
        mock_chat.return_value = {'message': {'content': 'Preheat oven to 350F.'}}

        ai_assistance.chef_ai.clear()

        # Call with extra leading/trailing whitespace
        res1 = ai_assistance.chef_ai("  How to bake a cake?  ")
        assert res1 == 'Preheat oven to 350F.'
        assert mock_chat.call_count == 1

        # Calling with stripped string should hit the cache because input is normalized
        res2 = ai_assistance.chef_ai("How to bake a cake?")
        assert res2 == 'Preheat oven to 350F.'
        assert mock_chat.call_count == 1
