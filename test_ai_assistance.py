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
        assert mock_chat.call_count == 1

def test_chef_ai_caching_with_input_normalization():
    with patch("ollama.chat") as mock_chat:
        mock_chat.return_value = {'message': {'content': 'Crack egg into boiling water.'}}

        # Clear Streamlit cache for test isolation
        ai_assistance.chef_ai.clear()

        # Initial call with mixed casing and standard spacing
        res1 = ai_assistance.chef_ai("How to poach an egg?")
        assert res1 == 'Crack egg into boiling water.'
        assert mock_chat.call_count == 1

        # Identical question with leading/trailing spaces and lower case
        res2 = ai_assistance.chef_ai("   how to poach an egg?   ")
        assert res2 == 'Crack egg into boiling water.'
        assert mock_chat.call_count == 1  # Cache hit, no redundant ollama call

        # Identical question with irregular spacing and upper case
        res3 = ai_assistance.chef_ai("HOW   TO   POACH   AN   EGG?")
        assert res3 == 'Crack egg into boiling water.'
        assert mock_chat.call_count == 1  # Cache hit, no redundant ollama call
