import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Define system prompt as a module-level constant to prevent repeated string allocations
# and dictionary creations on every LLM call execution.
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
# Query input is normalized before/during call to maximize Streamlit cache key hits
# for inputs differing only by surrounding whitespace.
@st.cache_data(show_spinner="Asking Chef AI...")
def chef_ai(question):
    clean_question = question.strip() if question else ""
    if not clean_question:
        return ""
    response = ollama.chat(
        model='mistral',
        messages=[
            CHEF_SYSTEM_PROMPT,
            {
                'role': 'user',
                'content': clean_question
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
