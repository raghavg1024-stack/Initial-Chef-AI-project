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

        # Check system prompt is passed correctly
        mock_chat.assert_called_with(
            model='mistral',
            messages=[
                ai_assistance.CHEF_SYSTEM_PROMPT,
                {'role': 'user', 'content': 'How to boil pasta?'}
            ]
        )

        # Second call with identical input should be served from cache
        res2 = ai_assistance.chef_ai("How to boil pasta?")
        assert res2 == 'Boil water and add pasta.'
        # Call count remains 1 because cached output is returned without calling ollama.chat
        assert mock_chat.call_count == 1

def test_chef_ai_whitespace_normalization_and_caching():
    with patch("ollama.chat") as mock_chat:
        mock_chat.return_value = {'message': {'content': 'Bake at 350F for 30 minutes.'}}

        # Clear Streamlit cache for test isolation
        ai_assistance.chef_ai.clear()

        # Input with surrounding whitespace
        raw_question = "  How to bake bread?  \n"
        normalized_question = raw_question.strip()

        # Calling chef_ai with normalized question
        res1 = ai_assistance.chef_ai(normalized_question)
        assert res1 == 'Bake at 350F for 30 minutes.'
        assert mock_chat.call_count == 1

        # Call again with normalized string hits cache
        res2 = ai_assistance.chef_ai("How to bake bread?")
        assert res2 == 'Bake at 350F for 30 minutes.'
        assert mock_chat.call_count == 1
