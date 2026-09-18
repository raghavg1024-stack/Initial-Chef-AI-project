import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Reusable system prompt constant to avoid dict and multiline string allocations on every call.
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
# Cache response results with @st.cache_data so duplicate/identical cooking queries
# do not trigger redundant and expensive calls to the Ollama LLM backend.
@st.cache_data(show_spinner="Asking Chef AI...")
def chef_ai(question):
    cleaned_question = question.strip() if question else ""
    if not cleaned_question:
        return ""
    response = ollama.chat(
        model='mistral',
        messages=[
            CHEF_SYSTEM_PROMPT,
            {
                'role': 'user',
                'content': cleaned_question
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    cleaned_question = question.strip() if question else ""
    if cleaned_question:
        st.write(chef_ai(cleaned_question))
    else:
        st.warning("Please enter a cooking question.")
