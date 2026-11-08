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
# 1. Reuse Ollama Client instance across runs via @st.cache_resource for persistent connection pooling.
# 2. Bound cache size (max_entries=256) and set TTL (1h) to prevent memory leaks from unbounded queries.
# 3. Normalize question query (whitespace & case) so variations like "How to boil pasta?" and
#    "how to boil pasta?" hit the cache instead of triggering redundant, expensive LLM calls.
@st.cache_resource
def get_ollama_client():
    return ollama.Client()

@st.cache_data(show_spinner="Asking Chef AI...", max_entries=256, ttl=3600)
def _cached_chef_ai(prompt: str):
    client = get_ollama_client()
    response = client.chat(
        model='mistral',
        messages=[
            {
                'role': 'system',
                'content': SYSTEM_PROMPT
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )
    return response['message']['content']

def chef_ai(question: str) -> str:
    if not question or not question.strip():
        return ""
    # Normalize internal spaces, leading/trailing whitespace, and case
    normalized_question = " ".join(question.strip().lower().split())
    return _cached_chef_ai(normalized_question)

# Expose clear method on chef_ai for test isolation and cache eviction
chef_ai.clear = _cached_chef_ai.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
