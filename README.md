# 🤖 Jonty - Personal AI Assistant

A personal, **completely offline** AI assistant that understands your local files and performs tasks on command.

## 🎯 Vision

Your own Jarvis-style AI that:
- 📂 Indexes and searches **all your local files** (PDF, txt, code, docs, etc.)
- 🧠 Understands queries using offline LLM (TinyLlama → LLaMA 3)
- 🛠️ Performs actions (calculator, alarms, file operations)
- 🔒 **100% offline** - No data leaves your computer
- ⚡ Runs on CPU-only systems

---

## 🏗️ Architecture

```
User Query
    ↓
🧠 Agent (Router)
    ├── 🔍 RAG (File Search) ← YOU ARE HERE
    ├── 🧰 Tools (Actions)
    ├── 💾 Memory
    ↓
📊 Context Builder
    ↓
🤖 LLM Brain
    ↓
Response
```

---

## 📋 Phase 1: Data Engine (CURRENT)

### Components

| Component | Purpose |
|-----------|---------|
| **loader.py** | Load various file formats (PDF, TXT, MD, DOCX, CSV, XLSX) |
| **chunker.py** | Split documents into manageable chunks with overlap |
| **embedder.py** | Convert text to vector embeddings |
| **vector_db.py** | FAISS-based vector storage & retrieval |
| **retriever.py** | Search functionality for RAG |
| **indexer.py** | Orchestrate the entire pipeline |

### Data Flow

```
Files (PDF, TXT, etc.)
    ↓ [Loader]
Text Content
    ↓ [Chunker]
Text Chunks
    ↓ [Embedder]
Vector Embeddings
    ↓ [Vector DB]
FAISS Index + Metadata
    ↓ [Retriever]
Search Results
    ↓ [Context for LLM]
```

---

## 🚀 Quick Start

### 1. Setup
```bash
cd ~/AI/jonty

# Create & activate environment (if not done)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Paths
Edit `config.yaml`:
```yaml
paths:
  - ~/Documents
  - ~/Downloads
  - ~/.
```

### 3. Index Your Files
```bash
python3 indexer.py
```

### 4. Test the System
```bash
python3 test_phase1.py
```

### 5. Use in Code
```python
from indexer import Indexer
from agent.retriever import Retriever

# Initialize
indexer = Indexer()
indexer.index_paths()

retriever = Retriever(indexer.embedder, indexer.vector_db)

# Search
results = retriever.search("your question here")
for result in results:
    print(f"{result['source']}: {result['text']}")
```

---

## ⚙️ Configuration

### config.yaml

```yaml
# Scan these folders
paths:
  - ~/Documents
  - ~/Downloads

# Embedding model (CPU-optimized, 384-dim)
embedding:
  model_name: "sentence-transformers/all-MiniLM-L6-v2"

# Vector database
vector_db:
  chunk_size: 512      # Characters per chunk
  overlap: 50          # Overlap for context
```

---

## 📊 Supported File Types

| Format | Method | Status |
|--------|--------|--------|
| PDF | PyMuPDF | ✅ Working |
| TXT, MD, PY, JSON | Direct read | ✅ Working |
| DOCX | python-docx | ✅ Working |
| CSV | Pandas | ✅ Working |
| XLSX/XLS | Pandas | ✅ Working |
| Images (OCR) | Tesseract | 🔧 Optional |

---

## 🧪 Testing

### Run Phase 1 Tests
```bash
python3 test_phase1.py
```

### Test Individual Components
```python
from agent.loader import FileLoader
from agent.chunker import TextChunker
from agent.embedder import Embedder

loader = FileLoader()
docs = loader.load_directory("~/Documents")

chunker = TextChunker()
chunks = chunker.chunk_documents(docs)

embedder = Embedder()
embeddings, chunks = embedder.embed_chunks(chunks)
```

---

## 🔄 Phases Overview

### ✅ Phase 1: Data Engine
- File loader & chunker
- Embeddings (FAISS)
- RAG retrieval
- Status: **COMPLETE**

### 🔲 Phase 2: AI Brain
- LLM integration
- Model loading (TinyLlama)
- Prompt system

### 🔲 Phase 3: Tools
- Calculator
- Alarms
- File operations

### 🔲 Phase 4: Agent
- Intent detection
- Smart routing

### 🔲 Phase 5: UI
- Streamlit interface

### 🔲 Phase 6: Upgrades
- LLaMA 3 (GPU)
- Whisper (audio)
- Vision models

---

## 💾 Project Structure

```
jonty/
├── agent/
│   ├── __init__.py
│   ├── loader.py          # File loading
│   ├── chunker.py         # Text chunking
│   ├── embedder.py        # Embeddings
│   ├── vector_db.py       # FAISS storage
│   ├── retriever.py       # Search
│   └── tools.py           # (Phase 3)
│
├── indexer.py             # Main orchestrator
├── config.yaml            # Configuration
├── requirements.txt       # Dependencies
├── test_phase1.py         # Tests
│
├── models/                # LLM models (Phase 2)
├── vector_db/             # FAISS index & metadata
├── logs/                  # Application logs
├── venv/                  # Python virtual environment
└── README.md              # This file
```

---

## 🎓 How It Works

### Indexing Process
1. **Loader**: Reads files (PDF, TXT, DOCX, etc.)
2. **Chunker**: Splits text into 512-char chunks with 50-char overlap
3. **Embedder**: Converts text to 384-dim vectors (all-MiniLM-L6-v2)
4. **Vector DB**: Stores vectors + metadata in FAISS

### Search Process
1. **Query**: User asks a question
2. **Embed**: Convert query to vector
3. **Search**: Find top-5 similar chunks in FAISS
4. **Rank**: Score by similarity (0-1)
5. **Return**: Relevant document chunks

---

## 🔥 Key Features

✅ **Offline**: No internet required
✅ **Fast**: CPU-optimized embeddings
✅ **Scalable**: FAISS handles millions of vectors
✅ **Flexible**: Supports multiple file types
✅ **Accurate**: Using state-of-the-art embeddings
✅ **Extensible**: Easy to add tools & features

---

## 📈 Performance (Benchmarks)

| Operation | Time | Notes |
|-----------|------|-------|
| Embed 1000 texts | ~2-3s | CPU-based |
| Search FAISS | <10ms | Regardless of index size |
| Load PDF (10 pages) | ~200ms | Using PyMuPDF |
| Index 100 files | 1-2min | Depends on size |

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'faiss'"
**Solution:**
```bash
source venv/bin/activate
pip install faiss-cpu
```

### Issue: Out of memory
**Solution:** Your RAM is limited (3.7GB). Use:
- Smaller chunk size: 256 instead of 512
- Lighter model: DistilBERT instead of all-MiniLM

### Issue: Slow indexing
**Solution:**
- Index specific folder instead of all paths
- Increase chunk_size to reduce number of chunks
- Use SSD instead of HDD

---

## 🚀 Next Steps

1. **Test Phase 1**: Run `python3 test_phase1.py`
2. **Phase 2**: Build LLM integration (model loading)
3. **Phase 3**: Add tools system
4. **Phase 4**: Implement agent router
5. **Phase 5**: Create UI

---

## 📚 Resources

- [FAISS Documentation](https://faiss.ai/)
- [Sentence-Transformers](https://www.sbert.net/)
- [RAG Explained](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
- [Vector Databases](https://www.pinecone.io/learn/vector-database/)

---

## 📝 License

Personal project - Feel free to use and modify!

---

## 🎯 Final Vision

```
┌─────────────────────────────────┐
│  "Hey Jonty, find files about   │
│   machine learning in my home"  │
└──────────────┬──────────────────┘
               ↓
        🧠 Jonty Brain
               ↓
    ┌─────────────────────┬──────────────┐
    ↓                     ↓              ↓
 [Search]            [Analyze]      [Execute]
 Files               Context         Actions
    ↓                 ↓              ↓
 🔍 FAISS         🤖 LLM Brain      🛠 Tools
    ↓                 ↓              ↓
 Top-K Results   Answer with     Calendar,
 with scores     predictions     Alarms,
                                 Files
                      ↓
            📱 Response to User
```

**Built with ❤️ for personal AI**
