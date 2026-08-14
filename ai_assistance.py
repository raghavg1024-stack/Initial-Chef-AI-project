import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

def chef_ai(question):
    try:
        response = ollama.chat(
            model='mistral',
            messages=[
                {
                    'role': 'system',
                    'content': """ You are a chef.
                    rules:
                        - Be polite and friendly
                        - Keep answers short and to the point
                        - Suggest recipes and cooking tips
                    """
                },
                {
                    'role': 'user',
                    'content': question
                }
            ]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error connecting to Chef AI: {e}"

if st.button("Send"):
    if question.strip():
        with st.spinner("Thinking..."):
            ans = chef_ai(question)
            if ans.startswith("Error connecting to Chef AI:"):
                st.error(ans)
            else:
                st.write(ans)
    else:
        st.warning("Please enter a question before sending.")