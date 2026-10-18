## 2025-05-10 - LLM Prompt Whitespace Cleanup
**Learning:** Multiline raw triple-quote string literals in system prompts can silently add unnecessary spaces, indents, and newlines into the request payload sent to LLM backends (like Ollama).
**Action:** Always clean and tightly format prompt strings sent to LLMs to prevent wasted input tokens and unnecessary network payload overhead.
