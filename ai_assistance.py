import ollama
import streamlit as st

# Bolt ⚡ Optimization:
# Reuse module-level constant for system prompt to avoid recreating dict on every LLM call.
SYSTEM_PROMPT = {
    'role': 'system',
    'content': """ You are a chef.
                rules:
                    - Be polite and friendly
                    - Keep answers short and to the point
                    - Suggest recipes and cooking tips
                """
}

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Cache response results with @st.cache_data so duplicate/identical cooking queries
# do not trigger redundant and expensive calls to the Ollama LLM backend.
# Input question is normalized before calling chef_ai to ensure whitespace variations share the cache key.
@st.cache_data(show_spinner="Asking Chef AI...")
def chef_ai(question):
    normalized = question.strip() if question else ""
    if not normalized:
        return ""
    response = ollama.chat(
        model='mistral',
        messages=[
            SYSTEM_PROMPT,
            {
                'role': 'user',
                'content': normalized
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
