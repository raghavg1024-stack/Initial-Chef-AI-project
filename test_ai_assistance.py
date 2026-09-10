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

        # Verify that static SYSTEM_MESSAGE was passed to ollama.chat
        args, kwargs = mock_chat.call_args
        assert kwargs['messages'][0] == ai_assistance.SYSTEM_MESSAGE

        # Second call with identical input should be served from cache
        res2 = ai_assistance.chef_ai("How to boil pasta?")
        assert res2 == 'Boil water and add pasta.'
        # Call count remains 1 because cached output is returned without calling ollama.chat
        assert mock_chat.call_count == 1

def test_chef_ai_normalized_input_caching():
    with patch("ollama.chat") as mock_chat:
        mock_chat.return_value = {'message': {'content': 'Bake at 350 degrees.'}}

        ai_assistance.chef_ai.clear()

        # Pass stripped input as done in the Streamlit UI handler
        q_clean = "How to bake a cake?   ".strip()
        res1 = ai_assistance.chef_ai(q_clean)
        assert res1 == 'Bake at 350 degrees.'
        assert mock_chat.call_count == 1

        # Subsequent call with normalized input should hit cache
        res2 = ai_assistance.chef_ai("How to bake a cake?")
        assert res2 == 'Bake at 350 degrees.'
        assert mock_chat.call_count == 1
