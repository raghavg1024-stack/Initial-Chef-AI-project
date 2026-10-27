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

        # Verify system prompt constant is passed
        called_args, called_kwargs = mock_chat.call_args
        assert called_kwargs['messages'][0]['content'] == ai_assistance.CHEF_SYSTEM_PROMPT

        # Second call with identical input should be served from cache
        res2 = ai_assistance.chef_ai("How to boil pasta?")
        assert res2 == 'Boil water and add pasta.'
        # Call count remains 1 because cached output is returned without calling ollama.chat
        assert mock_chat.call_count == 1

def test_chef_ai_whitespace_normalized_caching():
    with patch("ollama.chat") as mock_chat:
        mock_chat.return_value = {'message': {'content': 'Bake for 30 minutes.'}}

        ai_assistance.chef_ai.clear()

        # Calling chef_ai with normalized string
        question_clean = "How to bake bread?".strip()
        res1 = ai_assistance.chef_ai(question_clean)
        assert res1 == 'Bake for 30 minutes.'
        assert mock_chat.call_count == 1

        # Calling chef_ai with same normalized string (e.g. from UI cleaned input)
        question_with_spaces = "  How to bake bread?  ".strip()
        res2 = ai_assistance.chef_ai(question_with_spaces)
        assert res2 == 'Bake for 30 minutes.'
        assert mock_chat.call_count == 1
