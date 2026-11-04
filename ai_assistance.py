import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# 1. Hoist constant system message prompt to avoid redundant dictionary allocations.
# 2. Canonicalize query input (strip whitespace) before cache lookup so queries like
#    "how to boil pasta" and "how to boil pasta   " share the same cache key.
# 3. Limit cache size with `max_entries=256` to prevent unbounded memory growth.
SYSTEM_MESSAGE = {
    'role': 'system',
    'content': """ You are a chef.
                rules:
                    - Be polite and friendly
                    - Keep answers short and to the point
                    - Suggest recipes and cooking tips
                """
}

@st.cache_data(show_spinner="Asking Chef AI...", max_entries=256)
def chef_ai(question: str):
    cleaned = question.strip() if question else ""
    if not cleaned:
        return ""
    # Ensure cache key is canonicalized: if input had untrimmed whitespace,
    # delegate to the trimmed key so it hits the same cached entry.
    if question != cleaned:
        return chef_ai(cleaned)

    response = ollama.chat(
        model='mistral',
        messages=[
            SYSTEM_MESSAGE,
            {
                'role': 'user',
                'content': cleaned
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
