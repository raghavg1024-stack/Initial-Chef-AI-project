import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Cache response results with @st.cache_data so duplicate/identical cooking queries
# do not trigger redundant and expensive calls to the Ollama LLM backend.
# Query normalization (trimming whitespace and lowercasing) is performed BEFORE cache keying
# so that case-insensitive or whitespace-varied questions hit the cache, saving LLM latency.
@st.cache_data(show_spinner="Asking Chef AI...")
def _chef_ai_cached(question_normalized: str) -> str:
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
                'content': question_normalized
            }
        ]
    )
    return response['message']['content']


def chef_ai(question: str) -> str:
    if not question or not question.strip():
        return ""
    # Normalize string before calling cached function to maximize cache hit rate
    normalized_question = question.strip().lower()
    return _chef_ai_cached(normalized_question)


# Maintain backward compatibility for cache clearing in tests and Streamlit
chef_ai.clear = _chef_ai_cached.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
