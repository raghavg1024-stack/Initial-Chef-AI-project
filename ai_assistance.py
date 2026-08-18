import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Extract static system prompt outside the function to avoid recreating it on every call
SYSTEM_PROMPT = """ You are a chef.
rules:
    - Be polite and friendly
    - Keep answers short and to the point
    - Suggest recipes and cooking tips
"""


# Cache the LLM response for identical questions using Streamlit's cache_data.
# This prevents costly, high-latency Ollama API calls when repeated questions are queried or during Streamlit UI re-renders.
@st.cache_data(show_spinner=False)
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
