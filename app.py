import streamlit as st
import os                      # Added for absolute path handling
import time                    # Added for smoother streaming
import warnings
# Suppress HuggingFace symlink warning on Windows
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")

from ui.sidebar import render_sidebar
from ui.styles import apply_styles
from core.rag_pipeline import get_rag_response, index_document

# ✅ Base directory & Icon
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(BASE_DIR, "images", "image.png")

# ----------------------------
# 1️⃣ Page Config
# ----------------------------
st.set_page_config(
    page_title="RAG Document Assistant",
    page_icon=icon_path,
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_styles()

# ----------------------------
# 2️⃣ Sidebar
# ----------------------------
st.sidebar.image(icon_path, width=150)
page = render_sidebar()

# ----------------------------
# 3️⃣ HOME PAGE
# ----------------------------
if page == "Home":

    st.markdown("""
        <div style='text-align: center; padding-bottom: 20px;'>
            <h1 style='color: #4F8BF9;'>🤖 RAG Document Assistant</h1>
            <p style='font-size: 1.2rem; color: #666;'>
                Secure, Private, and Intelligent Document Interaction
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ----------------------------
    # About Project
    # ----------------------------
    with st.container():
        st.info("🚀 **Upload documents and ask questions without your data leaving your local environment (mostly).**")

    # ----------------------------
    # Why Better (Privacy & Security)
    # ----------------------------
    st.subheader("🔐 Key Privacy & Security Features")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🛡️ Local Storage")
        st.write("Embeddings stored locally via FAISS. No external vector DBs.")
        
    with col2:
        st.markdown("### 🔒 No Logging")
        st.write("User documents are processed in memory and never permanently stored.")

    with col3:
        st.markdown("### 🌐 Private Search")
        st.write("Integrated DuckDuckGo search for anonymous web context.")

    # ----------------------------
    # Architecture Section
    # ----------------------------
    st.divider()
    st.subheader("🏗️ System Architecture Overview")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("#### 1️⃣ Upload")
        st.caption("PDF, DOCX, TXT, CSV")
    with c2:
        st.markdown("#### 2️⃣ Process")
        st.caption("Semantic Chunking & Embedding")
    with c3:
        st.markdown("#### 3️⃣ Retrieve")
        st.caption("FAISS Vector Search")
    with c4:
        st.markdown("#### 4️⃣ Generate")
        st.caption("Gemini 2.5 Flash Answer")

    # ----------------------------
    # Team Section
    # ----------------------------
    st.subheader("👨‍💻 Developer Team")

    col1, col2 = st.columns(2)

    # ✅ Absolute image paths
    varaha_image = os.path.join(BASE_DIR, "images", "varaha.jpg")
    tanishtha_image = os.path.join(BASE_DIR, "images", "tanishtha.jpg")

    with col1:
        st.image(varaha_image, width=200)
        st.markdown("""
        ### Varaha Bohra  
        **Team Leader**  
        AI & Backend Architecture  
        """)

    with col2:
        st.image(tanishtha_image, width=200)
        st.markdown("""
        ### Tanishtha Soni  
        Frontend & UI/UX  
        """)

    st.markdown("<hr>", unsafe_allow_html=True)


# ----------------------------
# 4️⃣ CHAT PAGE (Your existing RAG page)
# ----------------------------
elif page == "Chat":

    st.title("💬 Chat with your Documents")

    # ----------------------------
    # Controls (Search & Upload)
    # ----------------------------
    uploaded_file = st.sidebar.file_uploader(
        "📂 Upload your document",
        type=["pdf", "txt", "docx", "xlsx", "csv", "md"]
    )
    
    # ----------------------------
    # 🧠 Efficient Caching Logic
    # ----------------------------
    if uploaded_file:
        # Only process if it's a new file
        if "last_uploaded_file" not in st.session_state or st.session_state.last_uploaded_file != uploaded_file.name:
            with st.spinner("🧠 Processing document... (This happens only once)"):
                vectorstore, chunks = index_document(uploaded_file)
                st.session_state.vector_store = vectorstore
                st.session_state.chunks = chunks
                st.session_state.last_uploaded_file = uploaded_file.name
                st.sidebar.success("Document indexed successfully!")
    else:
        # Reset if file is removed
        if "last_uploaded_file" in st.session_state:
            del st.session_state.last_uploaded_file
            del st.session_state.vector_store
            del st.session_state.chunks

    if uploaded_file is not None:
        pass # Success message handled above

    # Clear Chat Button
    if st.sidebar.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

    # Search Toggle - Placed in main area for visibility
    enable_search = st.toggle("🌍 Enable Web Search", value=False)

    # ----------------------------
    # Chat Logic
    # ----------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Welcome Placeholder
    if not st.session_state.messages:
        st.markdown("""
        <div style='text-align: center; margin-top: 50px; color: #888;'>
            <h2>👋 Welcome!</h2>
            <p>Upload a document on the left to get started.</p>
        </div>
        """, unsafe_allow_html=True)

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input (Always visible)
    user_prompt = st.chat_input("Ask a question...")

    if user_prompt:
        # Show user message
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # 🔥 REAL RAG CALL
        with st.chat_message("assistant"):
            status_placeholder = st.empty()
            status_placeholder.markdown("Thinking... 🤔")

            # Retrieve cached data
            vectorstore = st.session_state.get("vector_store")
            chunks = st.session_state.get("chunks")

            # Get chat history (excluding the current message which was just appended)
            chat_history = st.session_state.messages[:-1]

            stream = get_rag_response(user_prompt, vectorstore, chunks, chat_history=chat_history, enable_search=enable_search)
            
            def stream_with_status():
                first = True
                for chunk in stream:
                    if first:
                        status_placeholder.empty()
                        first = False
                    yield chunk
                    time.sleep(0.005)  # Tiny delay to smooth out the UI rendering
            
            ai_response = st.write_stream(stream_with_status())
            status_placeholder.empty()

        st.session_state.messages.append({"role": "assistant", "content": ai_response})

