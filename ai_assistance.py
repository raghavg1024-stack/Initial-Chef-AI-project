import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

SYSTEM_PROMPT = """ You are a chef.
rules:
    - Be polite and friendly
    - Keep answers short and to the point
    - Suggest recipes and cooking tips
"""

# Bolt ⚡ Optimization:
# Cache LLM responses using normalized question key so whitespace variations
# hit the cache. Pass keep_alive='1h' to keep Ollama model loaded in memory to prevent
# expensive model cold-start load times.
@st.cache_data(show_spinner="Asking Chef AI...")
def _get_chef_ai_response(clean_question: str) -> str:
    response = ollama.chat(
        model='mistral',
        keep_alive='1h',
        messages=[
            {
                'role': 'system',
                'content': SYSTEM_PROMPT
            },
            {
                'role': 'user',
                'content': clean_question
            }
        ]
    )
    return response['message']['content']


def chef_ai(question: str) -> str:
    if not question or not question.strip():
        return ""
    return _get_chef_ai_response(question.strip())


# Delegate cache operations to internal cached function
chef_ai.clear = _get_chef_ai_response.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
