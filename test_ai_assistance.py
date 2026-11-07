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

        # Verify that the system message used matches SYSTEM_MESSAGE
        call_kwargs = mock_chat.call_args[1]
        assert call_kwargs['messages'][0] == ai_assistance.SYSTEM_MESSAGE
        assert call_kwargs['messages'][1]['content'] == 'How to boil pasta?'

def test_chef_ai_caching_with_surrounding_whitespace():
    with patch("ollama.chat") as mock_chat:
        mock_chat.return_value = {'message': {'content': 'Chop onions and fry in butter.'}}

        # Clear Streamlit cache for test isolation
        ai_assistance.chef_ai.clear()

        # Input with trailing/leading whitespace should normalize to the same cache key
        res1 = ai_assistance.chef_ai("How to make caramelized onions?")
        assert res1 == 'Chop onions and fry in butter.'
        assert mock_chat.call_count == 1

        # Identical query with spaces and newlines normalized via strip
        normalized_q = "   How to make caramelized onions?\n\t".strip()
        res2 = ai_assistance.chef_ai(normalized_q)
        assert res2 == 'Chop onions and fry in butter.'
        # Cache hit prevents second call to ollama.chat
        assert mock_chat.call_count == 1
