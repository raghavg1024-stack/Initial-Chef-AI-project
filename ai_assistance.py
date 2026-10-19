import ollama
import streamlit as st

# Bolt ⚡ Optimization:
# Define SYSTEM_PROMPT at module level to avoid re-allocating system prompt text
# and dictionary objects on every LLM query.
SYSTEM_PROMPT = """ You are a chef.
rules:
    - Be polite and friendly
    - Keep answers short and to the point
    - Suggest recipes and cooking tips
"""

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Cache response results with @st.cache_data so duplicate/identical cooking queries
# do not trigger redundant and expensive calls to the Ollama LLM backend.
@st.cache_data(show_spinner="Asking Chef AI...")
def chef_ai(question):
    if not question or not question.strip():
        return ""
    response = ollama.chat(
        model='mistral',
        messages=[
            {
                'role': 'system',
                'content': SYSTEM_PROMPT
            },
            {
                'role': 'user',
                'content': question.strip()
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    # Bolt ⚡ Optimization:
    # Normalize question (strip whitespace) before calling chef_ai() so queries with
    # leading/trailing whitespace variations hit the @st.cache_data cache instead of
    # causing cache misses and triggering unnecessary LLM backend calls.
    normalized_question = question.strip() if question else ""
    if normalized_question:
        st.write(chef_ai(normalized_question))
    else:
        st.warning("Please enter a cooking question.")
