import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Extract system prompt as a module-level constant to eliminate redundant string allocation per call.
CHEF_SYSTEM_PROMPT = """ You are a chef.
rules:
    - Be polite and friendly
    - Keep answers short and to the point
    - Suggest recipes and cooking tips
"""

# Bolt ⚡ Optimization:
# Cache response results with @st.cache_data so duplicate/identical cooking queries
# do not trigger redundant and expensive calls to the Ollama LLM backend.
@st.cache_data(show_spinner="Asking Chef AI...")
def _chef_ai_cached(question: str) -> str:
    response = ollama.chat(
        model='mistral',
        messages=[
            {
                'role': 'system',
                'content': CHEF_SYSTEM_PROMPT
            },
            {
                'role': 'user',
                'content': question
            }
        ]
    )
    return response['message']['content']

def chef_ai(question: str) -> str:
    cleaned_question = question.strip() if question else ""
    if not cleaned_question:
        return ""
    return _chef_ai_cached(cleaned_question)

# Expose clear() on chef_ai for cache invalidation / testing compatibility
chef_ai.clear = _chef_ai_cached.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
