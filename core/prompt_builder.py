def build_prompt(context, web_context, question):
    return f"""
You are a helpful AI assistant.

Answer ONLY from the provided context.
If not found, say:
"I could not find this information in the provided documents."

DOCUMENT CONTEXT:
{context}

WEB CONTEXT:
{web_context}

QUESTION:
{question}
"""
