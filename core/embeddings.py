from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from core.config import get_google_api_keys


def get_embeddings_model():
    """Get the Google Generative AI embeddings model."""
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=get_google_api_keys()
    )


def get_local_embeddings():
    """Get local HuggingFace embeddings for efficient semantic chunking."""
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def create_vectorstore(docs):
    """Create a FAISS vector store from documents."""
    embeddings = get_embeddings_model()
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore


def embed_text(text):
    """Generate embeddings for a text string."""
    embeddings = get_embeddings_model()
    embedding = embeddings.embed_query(text)
    return embedding
