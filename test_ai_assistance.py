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

        # Second call with identical input should be served from cache
        res2 = ai_assistance.chef_ai("How to boil pasta?")
        assert res2 == 'Boil water and add pasta.'
        # Call count remains 1 because cached output is returned without calling ollama.chat
        assert mock_chat.call_count == 1

def test_chef_ai_whitespace_normalization_caching():
    with patch("ollama.chat") as mock_chat:
        mock_chat.return_value = {'message': {'content': 'Boil water and add pasta.'}}

        ai_assistance.chef_ai.clear()

        # Normalizing question before passing to chef_ai (as done in UI) ensures cache hits
        raw_input_1 = "How to boil pasta?  "
        clean_input_1 = raw_input_1.strip()
        res1 = ai_assistance.chef_ai(clean_input_1)
        assert res1 == 'Boil water and add pasta.'
        assert mock_chat.call_count == 1

        raw_input_2 = "How to boil pasta?"
        clean_input_2 = raw_input_2.strip()
        res2 = ai_assistance.chef_ai(clean_input_2)
        assert res2 == 'Boil water and add pasta.'
        # Call count remains 1 because normalized inputs match Streamlit's cache key
        assert mock_chat.call_count == 1
