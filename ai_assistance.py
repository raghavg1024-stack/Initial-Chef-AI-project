import ollama
import streamlit as st

st.title("Chef AI")

# Bolt ⚡ Optimization:
# Hoist static system message prompt to module level to prevent redundant dict/string object allocations.
SYSTEM_MESSAGE = {
    'role': 'system',
    'content': """ You are a chef.
    rules:
        - Be polite and friendly
        - Keep answers short and to the point
        - Suggest recipes and cooking tips
    """
}

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# 1. Cache response results with @st.cache_data so duplicate/identical cooking queries
#    do not trigger redundant and expensive calls to the Ollama LLM backend.
# 2. Use keep_alive='1h' to keep the model warm in memory and avoid 2-5 second model loading delays on subsequent requests.
@st.cache_data(show_spinner="Asking Chef AI...")
def chef_ai(question):
    if not question or not question.strip():
        return ""
    response = ollama.chat(
        model='mistral',
        messages=[
            SYSTEM_MESSAGE,
            {
                'role': 'user',
                'content': question.strip()
            }
        ],
        keep_alive='1h'
    )
    return response['message']['content']

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
