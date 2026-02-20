# 📄 RAG Document Assistant

A Secure, Privacy-First Retrieval-Augmented Generation System built with Streamlit, LangChain, FAISS, and Gemini models.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🚀 Overview

RAG Document Assistant is an advanced Retrieval-Augmented Generation (RAG) system that allows users to upload documents (PDF, TXT, DOCX, CSV) and ask intelligent questions about their content. The system uses local vector storage (FAISS) for embeddings and Gemini AI for generating accurate, context-aware responses.

### Key Features

- **📤 Multiple File Format Support**: Upload PDF, TXT, DOCX, or CSV files
- **🔐 Privacy-First Design**: All embeddings stored locally, no external vector databases
- **🧠 Intelligent Retrieval**: Semantic search using Google Generative AI embeddings
- **🌐 Optional Web Search**: DuckDuckGo integration for expanded context
- **💬 Conversational Interface**: Streamlit-based chat UI
- **📊 Document Chunking**: Intelligent text splitting for better retrieval

- ## 🚀 Live Demo
🔗 https://sp0505-majorproject-vwthdxhxfzmkwyznczmn5o.streamlit.app/

---

## 🏗️ System Architecture

```bash
┌─────────────────────────────────────────────────────────────┐
│                        RAG Pipeline                          │
├─────────────────────────────────────────────────────────────┤
│  1️⃣ Upload    →  2️⃣ Chunk  →  3️⃣ Embed  →  4️⃣ Retrieve  │
│  Document         Document       → Vector     → Relevant    │
│                                    Store        Chunks       │
│                                                              │
│  5️⃣ Generate  ←  Context + Question                        │
│  Answer                                                        │
└─────────────────────────────────────────────────────────────┘
```

### Architecture Components

| Component        | Technology           | Description                                   |
| ---------------- | -------------------- | --------------------------------------------- |
| **Frontend**     | Streamlit            | Web UI for document upload and chat           |
| **Vector Store** | FAISS                | Local embedding storage and similarity search |
| **Embeddings**   | Google Generative AI | text-embedding-004 model                      |
| **LLM**          | Gemini 2.5 Flash     | AI response generation                        |
| **Web Search**   | DuckDuckGo           | Optional contextual web search                |

---

## 📁 Project Structure

```bash
RAG-Document-Assistant/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── TODO.md                  # Development tasks
│
├── core/                    # Core RAG components
│   ├── config.py           # Configuration and API key management
│   ├── embeddings.py       # Vector embeddings generation
│   ├── llm.py             # Gemini LLM integration
│   ├── loader.py          # Document loading utilities
│   ├── prompt_builder.py  # Prompt construction
│   ├── rag_pipeline.py   # Main RAG pipeline
│   ├── retriever.py      # FAISS retrieval logic
│   └── search_tool.py    # DuckDuckGo search integration
│
├── ingestion/              # Data ingestion pipeline
│   ├── chunker.py         # Text chunking utilities
│   ├── loader.py         # File loading
│   ├── pipeline.py       # Ingestion pipeline
│   └── vector_store.py   # FAISS vector store
│
├── pages/                  # Streamlit pages
│   └── 1_Chat.py         # Chat interface
│
├── ui/                     # UI components
│   ├── _init_.py
│   ├── sidebar.py        # Navigation sidebar
│   └── styles.py         # Custom CSS styles
│
└── images/                 # Static assets
    ├── varaha.jpg        # Team member image
    └── tanishtha.jpg     # Team member image
```

---

## 🛠️ Installation

### Prerequisites

- Python 3.11 or higher
- Google API Key (for Gemini models)
- Tesseract OCR (optional, for scanned PDFs)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/bohravara789-debugit/RAG-Document-Assistant.git
   cd RAG-Document-Assistant
   ```

2. **Create Virtual Environment** (Recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the project root:

   ```bash
   GOOGLE_API_KEY=your_google_api_key_here
   ```

   Or set it as an environment variable:

   ```bash
   # Linux/Mac
   export GOOGLE_API_KEY=your_key_here

   # Windows
   set GOOGLE_API_KEY=your_key_here
   ```

5. **Run the Application**

   ```bash
   streamlit run app.py
   ```

6. **Open in Browser**

   Navigate to `http://localhost:8501`

---

## 📦 Dependencies

### Core Dependencies

| Package                | Version | Purpose                  |
| ---------------------- | ------- | ------------------------ |
| streamlit              | ≥1.28   | Web UI framework         |
| google-generativeai    | ≥0.3    | Gemini AI integration    |
| langchain              | ≥0.1    | LLM framework            |
| langchain-core         | ≥0.1    | LangChain core           |
| langchain-google-genai | ≥0.1    | Google GenAI integration |
| langchain-community    | ≥0.1    | Community integrations   |
| faiss-cpu              | ≥1.7    | Vector database          |
| duckduckgo-search      | ≥3.9    | Web search               |

### Document Processing

| Package     | Version | Purpose                 |
| ----------- | ------- | ----------------------- |
| pdfplumber  | ≥0.10   | PDF text extraction     |
| python-docx | ≥0.8    | DOCX file parsing       |
| pandas      | ≥2.0    | CSV processing          |
| pytesseract | ≥0.3    | OCR for scanned PDFs    |
| pdf2image   | ≥1.16   | PDF to image conversion |

### Utility Packages

| Package       | Version | Purpose                      |
| ------------- | ------- | ---------------------------- |
| python-dotenv | ≥1.0    | Environment variable loading |
| numpy         | ≥1.24   | Numerical operations         |

---

## 🔧 Configuration

### Google API Key Setup

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your environment or `.env` file

### Streamlit Secrets (Optional)

For production deployments, you can use Streamlit's secrets management:

Create `.streamlit/secrets.toml`:

```toml[general]
GOOGLE_API_KEY = "your_api_key_here"
```

### OCR Configuration (Optional)

For scanned PDF support, install Tesseract OCR:

**Windows:**

```bash
# Download and install from https://github.com/UB-Mannheim/tesseract/wiki
# Add to PATH or specify path in code
```

**Linux:**

```bash
sudo apt-get install tesseract-ocr
```

**Mac:**

```bash
brew install tesseract
```

---

## 💻 Usage

### Home Page

The home page provides an overview of the project:

- Project description
- Security and privacy features
- System architecture
- Developer team information

### Chat Page

1. **Upload a Document**
   - Click the file uploader
   - Select PDF, TXT, DOCX, or CSV file
   - Wait for "Document Indexed Successfully" message

2. **Ask Questions**
   - Type your question in the chat input
   - The system will retrieve relevant chunks
   - Gemini generates an answer based on the context

3. **Enable Web Search** (Optional)
   - Toggle "Enable Web Search" in the sidebar
   - Provides additional context from web sources

### Example Questions

- "What is this document about?"
- "Summarize the key points"
- "Find information about [specific topic]"

---

## 🔐 Privacy & Security

### Why This System is More Secure & Private

1. **🏠 Local Vector Storage (FAISS)**
   - All embeddings stored locally
   - No external vector database
   - No third-party storage of your documents

2. **🔒 No Document Logging**
   - User documents are never permanently stored
   - No training on your uploaded data

3. **🧠 Secure Model Usage**
   - Uses official Gemini API
   - API keys stored securely using environment variables
   - No exposure of credentials

4. **🌐 Controlled Web Search**
   - Uses DuckDuckGo search without tracking
   - No personal profiling
   - No targeted data collection

5. **🧩 Transparent Architecture**
   - Fully open architecture
   - Clear separation between UI, logic, and embeddings
   - No hidden data pipelines

---

## 🐛 Troubleshooting

### Common Issues

#### 1. API Key Error

**Problem:** "Invalid API key" or "API key not found"

**Solution:**

- Verify your GOOGLE_API_KEY is set correctly
- Check the key has access to Gemini API
- Ensure no spaces in the key

#### 2. Import Errors

**Problem:** "Module not found" errors

**Solution:**

```bash
pip install -r requirements.txt
```

#### 3. PDF Text Extraction Issues

**Problem:** PDF content not being extracted

**Solution:**

- Check if PDF is scanned (requires OCR)
- Install Tesseract for scanned PDFs
- Try converting PDF to text first

#### 4. Memory Issues with Large Files

**Problem:** Application crashes with large files

**Solution:**

- Reduce chunk_size in the code
- Process documents in batches
- Use smaller embedding models

#### 5. Streamlit Port Already in Use

**Problem:** "Port 8501 is already in use"

**Solution:**

```bash
streamlit run app.py --port 8502
```

---

## 🔧 Development

### Running in Development Mode

```bash
streamlit run app.py --reload
```

### Adding New Features

1. **New File Formats**: Modify `core/loader.py`
2. **Custom Embeddings**: Update `core/embeddings.py`
3. **Different LLM**: Modify `core/llm.py`
4. **UI Enhancements**: Update `ui/styles.py`

### Testing

```bash
# Run Streamlit in debug mode
streamlit run app.py --logger.level=debug
```

---

## 📊 Performance Tips

1. **Chunk Size**: Adjust `chunk_size` in rag_pipeline.py (default: 1000)
2. **Chunk Overlap**: Modify `chunk_overlap` for better context (default: 200)
3. **Top K Results**: Adjust retrieval count in retriever.py (default: 4)
4. **Temperature**: Modify LLM temperature in llm.py (default: 0.3)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

MIT License - See LICENSE file for details.

---

## 👨‍💻 Developer Team

### Varaha Bohra

**Team Leader** - AI & Backend Architecture

### Tanishtha Soni

Frontend & UI/UX

---

## 🔗 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [Google Generative AI](https://cloud.google.com/generative-ai)
- [FAISS Documentation](https://faiss.ai/)
- [DuckDuckGo Search API](https://pypi.org/project/duckduckgo-search/)

---

## 🙏 Acknowledgments

- LangChain Community
- Google AI
- Streamlit Team
- All contributors

---

<p align="center">
  Made with ❤️ by RAG Document Assistant Team
</p>

