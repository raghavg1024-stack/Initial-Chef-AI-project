## 2026-10-24 - Hoist static LLM system prompt & clean prompt whitespace
**Learning:** In Streamlit + LLM integrations (e.g. Ollama), inline dictionary definitions for system prompts cause unnecessary object re-allocations on every execution and preserve extraneous indentation tokens sent to the LLM context window. Hoisting system prompts to top-level constants and cleaning whitespace saves token context overhead and payload size.
**Action:** Always extract constant prompt structures to module-level constants and normalize prompt whitespace when constructing LLM requests.
