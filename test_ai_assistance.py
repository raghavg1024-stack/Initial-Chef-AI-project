from unittest.mock import patch
import pytest

# We import chef_ai from ai_assistance module
from ai_assistance import chef_ai


def test_chef_ai_cached():
    with patch("ollama.chat") as mock_chat:
        mock_chat.return_value = {
            'message': {
                'content': 'Boil water, insert eggs, wait 6-10 minutes.'
            }
        }

        # Clear cache before testing to start with a clean state
        chef_ai.clear()

        question = "How to boil eggs?"
        result1 = chef_ai(question)
        result2 = chef_ai(question)

        assert result1 == 'Boil water, insert eggs, wait 6-10 minutes.'
        assert result2 == 'Boil water, insert eggs, wait 6-10 minutes.'

        # Ollama API should only be called ONCE due to @st.cache_data caching
        assert mock_chat.call_count == 1
