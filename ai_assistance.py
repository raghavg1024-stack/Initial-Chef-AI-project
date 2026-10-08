import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# 1. Hoist static system prompt to module scope to avoid re-allocating string and dict objects on every request.
# 2. Normalize input string before cache key evaluation so whitespace variations (e.g., "pasta " vs "pasta")
#    hit Streamlit's @st.cache_data cache instead of triggering redundant, expensive LLM calls to Ollama.
SYSTEM_PROMPT = """ You are a chef.
                rules:
                    - Be polite and friendly
                    - Keep answers short and to the point
                    - Suggest recipes and cooking tips
                """


@st.cache_data(show_spinner="Asking Chef AI...")
def _fetch_chef_response(clean_question: str) -> str:
    """Fetch response from Ollama model, cached by normalized question string."""
    response = ollama.chat(
        model='mistral',
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
    """Public interface for Chef AI query processing, normalizing input before checking cache."""
    if not question:
        return ""
    clean_question = question.strip()
    if not clean_question:
        return ""
    return _fetch_chef_response(clean_question)


# Maintain backwards compatibility and cache clearing functionality for chef_ai
chef_ai.clear = _fetch_chef_response.clear

if st.button("Send"):
    clean_q = question.strip() if question else ""
    if clean_q:
        st.write(chef_ai(clean_q))
    else:
        st.warning("Please enter a cooking question.")
