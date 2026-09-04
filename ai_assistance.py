import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Hoist static system prompt constant to avoid allocating it on every function call.
SYSTEM_PROMPT = """ You are a chef.
rules:
    - Be polite and friendly
    - Keep answers short and to the point
    - Suggest recipes and cooking tips
"""

# Bolt ⚡ Optimization:
# Cache response results with @st.cache_data so identical cooking queries
# do not trigger redundant and expensive calls to the Ollama LLM backend.
@st.cache_data(show_spinner="Asking Chef AI...")
def chef_ai(clean_question):
    if not clean_question:
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
                'content': clean_question
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    # Bolt ⚡ Optimization:
    # Normalize question string (strip leading/trailing whitespace) BEFORE passing to chef_ai
    # so queries like " pasta " and "pasta" share the same cache key in Streamlit @st.cache_data.
    clean_q = question.strip() if question else ""
    if clean_q:
        st.write(chef_ai(clean_q))
    else:
        st.warning("Please enter a cooking question.")
