import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

SYSTEM_PROMPT = (
    "You are a chef.\n"
    "rules:\n"
    "    - Be polite and friendly\n"
    "    - Keep answers short and to the point\n"
    "    - Suggest recipes and cooking tips"
)

# Bolt ⚡ Optimization:
# Cache response results with @st.cache_data on normalized question input.
# Normalizing whitespace prior to caching ensures identical queries with variable
# surrounding whitespace hit the cache, avoiding duplicate expensive LLM calls.
@st.cache_data(show_spinner="Asking Chef AI...")
def _chef_ai_cached(clean_question: str) -> str:
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
    if not question or not question.strip():
        return ""
    return _chef_ai_cached(question.strip())


# Expose cache invalidation hook for backwards compatibility and testing
chef_ai.clear = _chef_ai_cached.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
