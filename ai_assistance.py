import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Module-level static system prompt dictionary avoids re-creating string/dict allocations per call.
SYSTEM_PROMPT = {
    'role': 'system',
    'content': """ You are a chef.
                rules:
                    - Be polite and friendly
                    - Keep answers short and to the point
                    - Suggest recipes and cooking tips
                """
}

# Bolt ⚡ Optimization:
# Input queries are sanitized before being passed to this cached function.
# Normalizing whitespace before hashing ensures queries with leading/trailing spaces
# hit the cache rather than triggering redundant, expensive LLM calls.
@st.cache_data(show_spinner="Asking Chef AI...")
def _get_chef_response(clean_question: str) -> str:
    response = ollama.chat(
        model='mistral',
        messages=[
            SYSTEM_PROMPT,
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
    return _get_chef_response(question.strip())

# Expose .clear() on chef_ai for test/caller compatibility
chef_ai.clear = _get_chef_response.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
