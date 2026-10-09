import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Move static system prompt to module level to avoid re-allocating prompt strings on every request.
SYSTEM_PROMPT = """ You are a chef.
rules:
    - Be polite and friendly
    - Keep answers short and to the point
    - Suggest recipes and cooking tips
"""

@st.cache_data(show_spinner="Asking Chef AI...")
def _get_chef_ai_response(clean_question: str) -> str:
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

# Bolt ⚡ Optimization:
# Normalize question by stripping whitespace BEFORE passing to the cached function.
# This ensures whitespace variations (e.g., " How to cook rice? ") hit the same cache key
# and avoid redundant, expensive LLM calls.
def chef_ai(question: str) -> str:
    if not question:
        return ""
    clean_q = question.strip()
    if not clean_q:
        return ""
    return _get_chef_ai_response(clean_q)

# Expose clear() method on chef_ai for Streamlit cache management and test isolation
chef_ai.clear = _get_chef_ai_response.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
