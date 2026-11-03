import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

CHEF_SYSTEM_PROMPT = """ You are a chef.
rules:
    - Be polite and friendly
    - Keep answers short and to the point
    - Suggest recipes and cooking tips
"""

# Bolt ⚡ Optimization:
# 1. Cache response results with @st.cache_data so duplicate/identical cooking queries
#    do not trigger redundant and expensive calls to the Ollama LLM backend (~seconds per query).
# 2. Normalize question text (strip edge whitespace, collapse multiple spaces, lower-case)
#    before caching/querying so subtle variations in user input (e.g. "How to boil eggs?" vs
#    "how to boil eggs? " vs "How   to boil eggs?") hit the cache instead of running a full LLM inference.
@st.cache_data(show_spinner="Asking Chef AI...")
def _ask_chef(normalized_question: str) -> str:
    response = ollama.chat(
        model='mistral',
        messages=[
            {
                'role': 'system',
                'content': CHEF_SYSTEM_PROMPT
            },
            {
                'role': 'user',
                'content': normalized_question
            }
        ]
    )
    return response['message']['content']

def chef_ai(question: str) -> str:
    if not question or not question.strip():
        return ""
    # Normalize whitespace and casing to maximize cache hit rate
    normalized_question = " ".join(question.strip().lower().split())
    return _ask_chef(normalized_question)

# Preserve clear() method on chef_ai for cache management and test isolation
chef_ai.clear = _ask_chef.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
