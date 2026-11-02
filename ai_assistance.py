import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Pre-allocated system message to avoid recreating dictionary structures on every call
SYSTEM_MESSAGE = {
    'role': 'system',
    'content': """ You are a chef.
    rules:
        - Be polite and friendly
        - Keep answers short and to the point
        - Suggest recipes and cooking tips
    """
}

# Bolt ⚡ Optimization:
# 1. Cache LLM response results with @st.cache_data.
# 2. Limit cache memory growth with max_entries and ttl.
# 3. Cache on the stripped/normalized query so queries with varying leading/trailing
#    whitespaces (e.g. "pasta" vs "  pasta  ") hit the cache instead of triggering
#    expensive LLM API calls (~seconds saved per duplicate user prompt).
@st.cache_data(show_spinner="Asking Chef AI...", max_entries=500, ttl=3600)
def _cached_chef_ai(prompt: str) -> str:
    response = ollama.chat(
        model='mistral',
        messages=[
            SYSTEM_MESSAGE,
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )
    return response['message']['content']

def chef_ai(question: str) -> str:
    if not question:
        return ""
    normalized = question.strip()
    if not normalized:
        return ""
    return _cached_chef_ai(normalized)

# Retain st.cache_data helper methods on chef_ai for test isolation and cache controls
chef_ai.clear = _cached_chef_ai.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
