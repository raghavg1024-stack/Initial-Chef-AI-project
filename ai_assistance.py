import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Define system prompt at module level so dictionary and string objects are allocated once
# at load time rather than recreated on every function execution.
SYSTEM_MESSAGE = {
    'role': 'system',
    'content': (
        " You are a chef.\n"
        "rules:\n"
        "    - Be polite and friendly\n"
        "    - Keep answers short and to the point\n"
        "    - Suggest recipes and cooking tips\n"
        " "
    )
}

# Bolt ⚡ Optimization:
# Cache results by normalized/cleaned question string using @st.cache_data.
@st.cache_data(show_spinner="Asking Chef AI...")
def _get_chef_response(cleaned_question: str) -> str:
    response = ollama.chat(
        model='mistral',
        messages=[
            SYSTEM_MESSAGE,
            {
                'role': 'user',
                'content': cleaned_question
            }
        ]
    )
    return response['message']['content']

def chef_ai(question: str) -> str:
    """
    Bolt ⚡ Optimization:
    Sanitize and normalize the question input before cache lookup.
    This guarantees that queries with whitespace variations (e.g. "How to boil pasta?" and " How to boil pasta? ")
    share the exact same cache entry, avoiding duplicate expensive calls to the Ollama LLM backend.
    Blank/empty questions short-circuit immediately without populating cache entries.
    """
    if not question or not question.strip():
        return ""
    return _get_chef_response(question.strip())

# Forward Streamlit cache control methods for testing and backward compatibility
chef_ai.clear = _get_chef_response.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
