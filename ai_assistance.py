import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Extract static system prompt message as a module-level constant to prevent
# redundant dictionary and string allocations on cache-miss LLM invocations.
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
@st.cache_data(show_spinner="Asking Chef AI...")
def chef_ai(question):
    if not question or not question.strip():
        return ""

    clean_question = question.strip()

    response = ollama.chat(
        model='mistral',
        messages=[
            SYSTEM_PROMPT,
            {
                'role': 'user',
                'content': clean_question
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    # Bolt ⚡ Optimization:
    # Pass question.strip() so inputs with leading/trailing whitespace resolve to
    # the same cache key in @st.cache_data and avoid redundant LLM calls.
    clean_q = question.strip() if question else ""
    if clean_q:
        st.write(chef_ai(clean_q))
    else:
        st.warning("Please enter a cooking question.")
