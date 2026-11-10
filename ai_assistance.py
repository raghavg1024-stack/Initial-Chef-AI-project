import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Pre-define the static system prompt at module level so it is not repeatedly
# allocated on each invocation of the chat endpoint.
SYSTEM_PROMPT = """ You are a chef.
rules:
    - Be polite and friendly
    - Keep answers short and to the point
    - Suggest recipes and cooking tips
"""

# Bolt ⚡ Optimization:
# Cache response results with @st.cache_data so duplicate/identical cooking queries
# do not trigger redundant and expensive calls to the Ollama LLM backend.
# The question argument is stripped before being passed or cached to prevent cache
# misses caused solely by leading/trailing whitespace variations.
@st.cache_data(show_spinner="Asking Chef AI...")
def chef_ai(question):
    stripped_question = question.strip() if question else ""
    if not stripped_question:
        return ""
    response = ollama.chat(
        model='mistral',
        messages=[
            {
                'role': 'system',
                'content': SYSTEM_PROMPT
            },
            {
                'role': 'user',
                'content': stripped_question
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    normalized_question = question.strip() if question else ""
    if normalized_question:
        # Pass normalized (stripped) query so identical queries with varying
        # whitespace reuse the cache instead of triggering an expensive LLM call.
        st.write(chef_ai(normalized_question))
    else:
        st.warning("Please enter a cooking question.")
