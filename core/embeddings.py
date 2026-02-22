from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from core.config import get_google_api_keys


def get_embeddings_model(api_key):
    """Get the Google Generative AI embeddings model."""
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key
    )


def get_local_embeddings():
    """Get local HuggingFace embeddings for efficient semantic chunking."""
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def create_vectorstore(docs):
    """Create a FAISS vector store from documents."""
    api_keys = get_google_api_keys()
    if not api_keys:
        raise ValueError("No Google API keys found. Please check secrets.toml.")

    last_error = None
    for i, key in enumerate(api_keys):
        try:
            embeddings = get_embeddings_model(key)
            vectorstore = FAISS.from_documents(docs, embeddings)
            return vectorstore
        except Exception as e:
            print(f"⚠️ Key #{i+1} failed for embeddings: {e}")
            last_error = e
            continue
    
    if last_error:
        raise last_error


def embed_text(text):
    """Generate embeddings for a text string."""
    api_keys = get_google_api_keys()
    if not api_keys:
        raise ValueError("No Google API keys found. Please check secrets.toml.")

    last_error = None
    for i, key in enumerate(api_keys):
        try:
            embeddings = get_embeddings_model(key)
            embedding = embeddings.embed_query(text)
            return embedding
        except Exception as e:
            print(f"⚠️ Key #{i+1} failed for embeddings: {e}")
            last_error = e
            continue
            
    if last_error:
        raise last_error
