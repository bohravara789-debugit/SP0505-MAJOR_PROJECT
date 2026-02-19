from ingestion.loader import load_document
from core.embeddings import create_vectorstore, get_embeddings_model, get_local_embeddings
from core.llm import generate_answer

from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.tools import DuckDuckGoSearchRun

def index_document(file):
    """
    Processes the uploaded file: loads, splits, and creates a vector store.
    Returns (vectorstore, split_docs) to be cached in session state.
    """
    if not file:
        return None, []

    documents = load_document(file)
    if not documents:
        return None, []

    split_docs = []

    try:
        # Try Semantic Chunking first
        splitter = SemanticChunker(get_local_embeddings())
        split_docs = splitter.split_documents(documents)
    except Exception as e:
        # Handle Rate Limits (429) by falling back to standard splitter
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            print("⚠️ Quota exceeded for Semantic Chunking. Falling back to standard chunking.")
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            split_docs = splitter.split_documents(documents)
        else:
            raise e

    if split_docs:
        # 3️⃣ Create vector store
        vectorstore = create_vectorstore(split_docs)
        return vectorstore, split_docs
    
    return None, []


def get_rag_response(query, vectorstore=None, chunks=None, chat_history=None, enable_search=False):
    """
    Generates an answer using the pre-computed vectorstore.
    """
    docs = []

    # 4️⃣ Retrieve relevant docs
    if vectorstore:
        # Retrieve top 15 chunks
        docs = vectorstore.similarity_search(query, k=15)
        
        # Always include the beginning of the doc where Table of Contents usually lives
        if chunks:
            docs.extend(chunks[:2])

    # 4.5️⃣ Web Search (Optional)
    if enable_search:
        try:
            search = DuckDuckGoSearchRun()
            web_results = search.run(query)
            docs.append(Document(page_content=f"Web Search Results:\n{web_results}", metadata={"source": "DuckDuckGo"}))
        except Exception:
            pass  # Continue if search fails

    # 5️⃣ Generate answer
    if docs:
        context_text = "\n\n".join([doc.page_content for doc in docs])
    else:
        context_text = "No specific document context provided. Answer based on general knowledge."
        
    # Format Chat History
    history_text = ""
    if chat_history:
        for msg in chat_history[-10:]:  # Include last 10 messages for context
            role = "User" if msg["role"] == "user" else "Assistant"
            history_text += f"{role}: {msg['content']}\n"
    
    if not history_text:
        history_text = "No previous conversation."

    # Improved Prompt Engineering
    prompt = f"""You are an intelligent AI assistant specialized in analyzing documents.

### Instructions:
1. **Context-Driven**: Answer the question primarily using the information provided in the 'Context' section below.
2. **Conversation Aware**: Use the 'Chat History' to understand the conversation context (e.g., follow-up questions, references to previous topics).
3. **Comprehensive**: Synthesize information from multiple parts of the context if needed.
4. **Structured**: Use Markdown (headers, lists, bold text) to organize your response clearly.
5. **Honesty**: If the context does not contain the answer, state: "I couldn't find specific information regarding this in the provided documents."
6. **General Knowledge**: If the context is empty or irrelevant, you may provide a general answer, but clarify that it is not based on the document.

### Context:
{context_text}

### Chat History:
{history_text}

### Question:
{query}

### Answer:"""

    response_stream = generate_answer(prompt)

    for chunk in response_stream:
        try:
            if hasattr(chunk, "text") and chunk.text:
                yield chunk.text
        except Exception:
            # Skip chunks blocked by safety filters to prevent crashing
            pass
