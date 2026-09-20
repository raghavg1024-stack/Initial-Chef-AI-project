import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

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
# Normalizing input whitespace before caching ensures queries with extra spaces hit the cache.
@st.cache_data(show_spinner="Asking Chef AI...")
def chef_ai(question):
    if not question:
        return ""
    normalized_question = question.strip()
    if not normalized_question:
        return ""
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

if st.button("Send"):
    normalized = question.strip() if question else ""
    if normalized:
        st.write(chef_ai(normalized))
    else:
        st.warning("Please enter a cooking question.")
