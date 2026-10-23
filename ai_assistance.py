import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Module-level constant for system prompt to avoid recreating message dict on every call.
SYSTEM_PROMPT = {
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
# Normalizing input strings prior to calling chef_ai maximizes Streamlit cache hit rate.
@st.cache_data(show_spinner="Asking Chef AI...")
def chef_ai(question):
    normalized_question = question.strip() if question else ""
    if not normalized_question:
        return ""
    response = ollama.chat(
        model='mistral',
        messages=[
            SYSTEM_PROMPT,
            {
                'role': 'user',
                'content': normalized_question
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    clean_question = question.strip() if question else ""
    if clean_question:
        st.write(chef_ai(clean_question))
    else:
        st.warning("Please enter a cooking question.")
