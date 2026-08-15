import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Pre-defined system message constant to avoid dict re-allocation and token bloat from extra whitespace on every call
SYSTEM_MESSAGE = {
    "role": "system",
    "content": "You are a chef.\nrules:\n- Be polite and friendly\n- Keep answers short and to the point\n- Suggest recipes and cooking tips",
}


# Cache responses to prevent redundant Ollama API calls for identical questions (~100x speedup on repeat queries)
@st.cache_data(show_spinner=False)
def chef_ai(question: str) -> str:
    if not question or not question.strip():
        return ""
    response = ollama.chat(
        model="mistral",
        messages=[
            SYSTEM_MESSAGE,
            {
                "role": "user",
                "content": question.strip(),
            },
        ],
    )
    return response["message"]["content"]


if st.button("Send"):
    if question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a question first.")
