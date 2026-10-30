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

        # Verify SYSTEM_MESSAGE constant was used in ollama.chat
        mock_chat.assert_called_with(
            model='mistral',
            messages=[
                ai_assistance.SYSTEM_MESSAGE,
                {
                    'role': 'user',
                    'content': 'How to boil pasta?'
                }
            ]
        )

        # Second call with identical input should be served from cache
        res2 = ai_assistance.chef_ai("How to boil pasta?")
        assert res2 == 'Boil water and add pasta.'
        # Call count remains 1 because cached output is returned without calling ollama.chat
        assert mock_chat.call_count == 1

def test_chef_ai_stripped_question_cache_hits():
    with patch("ollama.chat") as mock_chat:
        mock_chat.return_value = {'message': {'content': 'Bake at 350F for 20 minutes.'}}

        # Clear Streamlit cache
        ai_assistance.chef_ai.clear()

        q = "How to bake a cake?  "
        cleaned = q.strip()

        res1 = ai_assistance.chef_ai(cleaned)
        assert res1 == 'Bake at 350F for 20 minutes.'
        assert mock_chat.call_count == 1

        # Second call with pre-stripped input hits cache
        res2 = ai_assistance.chef_ai(cleaned)
        assert res2 == 'Bake at 350F for 20 minutes.'
        assert mock_chat.call_count == 1
