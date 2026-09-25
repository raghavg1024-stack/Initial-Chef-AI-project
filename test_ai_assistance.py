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

        # Check system prompt constant is used in call
        call_args = mock_chat.call_args[1]
        assert call_args['messages'][0]['content'] == ai_assistance.CHEF_SYSTEM_PROMPT

        # Second call with whitespace-padded query should be served from cache after normalization
        res2 = ai_assistance.chef_ai("  How to boil pasta?  ")
        assert res2 == 'Boil water and add pasta.'
        # Call count remains 1 because normalized query matches cached key
        assert mock_chat.call_count == 1
