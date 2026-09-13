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
        ai_assistance._get_chef_response.clear()

        # First call should invoke ollama.chat
        res1 = ai_assistance.chef_ai("How to boil pasta?")
        assert res1 == 'Boil water and add pasta.'
        assert mock_chat.call_count == 1

        # Identical query should be served from cache
        res2 = ai_assistance.chef_ai("How to boil pasta?")
        assert res2 == 'Boil water and add pasta.'
        assert mock_chat.call_count == 1

        # Query variation with different casing and whitespace should also be served from cache
        res3 = ai_assistance.chef_ai("  HOW TO BOIL PASTA?  ")
        assert res3 == 'Boil water and add pasta.'
        assert mock_chat.call_count == 1
