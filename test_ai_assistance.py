from unittest.mock import patch, MagicMock
import ai_assistance

def test_chef_ai_calls_ollama():
    mock_response = {
        'message': {
            'content': 'To make scrambled eggs, whisk eggs with milk and cook on low heat.'
        }
    }
    with patch('ollama.chat', return_value=mock_response) as mock_chat:
        # Call with a unique question to ensure cache miss on first call
        result = ai_assistance.chef_ai("How to make scrambled eggs?")
        assert result == 'To make scrambled eggs, whisk eggs with milk and cook on low heat.'
        mock_chat.assert_called_once()
        args, kwargs = mock_chat.call_args
        assert kwargs['model'] == 'mistral'
        assert kwargs['messages'][0]['role'] == 'system'
        assert kwargs['messages'][1] == {'role': 'user', 'content': "How to make scrambled eggs?"}

def test_chef_ai_caching():
    mock_response = {
        'message': {
            'content': 'Sear the steak on high heat for 3 minutes per side.'
        }
    }
    with patch('ollama.chat', return_value=mock_response) as mock_chat:
        question = "How to sear a steak?"
        res1 = ai_assistance.chef_ai(question)
        res2 = ai_assistance.chef_ai(question)

        assert res1 == 'Sear the steak on high heat for 3 minutes per side.'
        assert res2 == res1
        # Streamlit caching (@st.cache_data) should ensure ollama.chat is only called once
        assert mock_chat.call_count == 1
