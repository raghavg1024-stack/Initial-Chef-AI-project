import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Module-level constant for system prompt to avoid re-allocating on every function call or Streamlit rerun
SYSTEM_PROMPT = """ You are a chef.
rules:
    - Be polite and friendly
    - Keep answers short and to the point
    - Suggest recipes and cooking tips
"""

# Cache responses for identical questions to avoid redundant, expensive LLM calls to Ollama.
# Expected performance impact: Reduces response latency from seconds to <1ms for cached queries.
@st.cache_data
def chef_ai(question):
    response = ollama.chat(
        model='mistral',
        messages=[
            {
                'role': 'system',
                'content': SYSTEM_PROMPT
            },
            {
                'role': 'user',
                'content': question
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    st.write(chef_ai(question))
