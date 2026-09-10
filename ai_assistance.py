import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Module-level system message constant prevents dictionary and string re-allocation on every call.
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
    clean_question = question.strip()
    response = ollama.chat(
        model='mistral',
        messages=[
            SYSTEM_MESSAGE,
            {
                'role': 'user',
                'content': clean_question
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    clean_q = question.strip() if question else ""
    if clean_q:
        # Bolt ⚡ Optimization: Pass stripped query string to ensure identical cache key
        # in Streamlit's @st.cache_data even when input contains leading/trailing spaces.
        st.write(chef_ai(clean_q))
    else:
        st.warning("Please enter a cooking question.")
