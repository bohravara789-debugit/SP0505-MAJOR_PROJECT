from langchain_text_splitters import RecursiveCharacterTextSplitter

from ingestion.loader import load_document
from core.embeddings import create_vectorstore
from core.llm import generate_answer


def get_rag_response(query, file):

    # 1️⃣ Load document
    documents = load_document(file)

    # 2️⃣ Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    split_docs = splitter.split_documents(documents)

    # 3️⃣ Create vector store
    vectorstore = create_vectorstore(split_docs)

    # 4️⃣ Retrieve relevant docs
    docs = vectorstore.similarity_search(query)

    # 5️⃣ Generate answer
    answer = generate_answer(query, docs)

    return answer
