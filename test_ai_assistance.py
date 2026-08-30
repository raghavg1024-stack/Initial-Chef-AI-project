from unittest.mock import patch
from ai_assistance import chef_ai

def test_chef_ai():
    with patch("ollama.chat") as mock_chat:
        mock_chat.return_value = {
            'message': {
                'content': 'Preheat the oven to 350F.'
            }
        }

        # Test original invocation
        res1 = chef_ai("How to bake a cake?")
        assert res1 == "Preheat the oven to 350F."
        assert mock_chat.call_count == 1

        # Test cached invocation with duplicate input
        res2 = chef_ai("How to bake a cake?")
        assert res2 == "Preheat the oven to 350F."
        # Streamlit st.cache_data should cache the response, preventing second call to ollama.chat
        assert mock_chat.call_count == 1
