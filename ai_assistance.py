import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Hoist static system prompt outside the function to avoid re-allocating
# the system prompt dictionary on every LLM call.
CHEF_SYSTEM_PROMPT = {
    'role': 'system',
    'content': """ You are a chef.
    rules:
        - Be polite and friendly
        - Keep answers short and to the point
        - Suggest recipes and cooking tips
    """
}

# Bolt ⚡ Optimization:
# Cache responses keyed on normalized query strings (lowercased, collapsed whitespace).
# This prevents redundant, slow LLM calls when users submit semantically identical questions
# with variations in case or whitespace (e.g. "How to boil pasta?" vs "  how to boil pasta?  ").
@st.cache_data(show_spinner="Asking Chef AI...")
def _fetch_chef_ai_response(normalized_question: str) -> str:
    response = ollama.chat(
        model='mistral',
        messages=[
            CHEF_SYSTEM_PROMPT,
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
    # Normalize question by trimming, lowercasing, and collapsing multiple whitespaces
    normalized_question = " ".join(question.strip().lower().split())
    return _fetch_chef_ai_response(normalized_question)

# Expose cache clearance helper on chef_ai for test isolation and cache resets
chef_ai.clear = _fetch_chef_ai_response.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
