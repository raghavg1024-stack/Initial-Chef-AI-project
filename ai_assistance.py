import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Pre-allocated system message constant to avoid redundant object/dict re-creation on every call
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
# Cache response results with @st.cache_data so duplicate/identical cooking queries
# do not trigger redundant and expensive calls to the Ollama LLM backend.
@st.cache_data(show_spinner="Asking Chef AI...")
def chef_ai(question):
    if not question or not question.strip():
        return ""
    cleaned_question = question.strip()
    response = ollama.chat(
        model='mistral',
        messages=[
            SYSTEM_MESSAGE,
            {
                'role': 'user',
                'content': cleaned_question
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    if question and question.strip():
        # Bolt ⚡ Optimization: Pass stripped question to ensure queries with whitespace variations
        # hit the @st.cache_data cache instead of triggering redundant LLM calls.
        st.write(chef_ai(question.strip()))
    else:
        st.warning("Please enter a cooking question.")
