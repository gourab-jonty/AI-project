# 🤖 Jonty - Personal AI Assistant

A powerful **offline-first** personal AI assistant that understands your local files and performs actions.

## ✨ Features

- 🔍 **RAG (Retrieval-Augmented Generation)**: Search and understand your local files (PDFs, documents, code)
- 🧠 **Offline LLM**: Works completely offline using TinyLlama (CPU-friendly)
- 🧰 **Tools System**: Calculator, file operations, alarms, app launching
- 🤔 **Smart Agent**: Automatically decides between search, tools, or direct answers
- 💾 **Memory**: Remembers conversation context
- ⚡ **Lightweight & Portable**: Code is only ~50MB - quick setup on any machine (Windows/Mac/Linux)

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

## 🚀 Quick Setup Guide

### **On Current Machine (Linux)**
```bash
cd /home/gourab-nandi/AI/jonty
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### **On New Machine (Windows/Linux/Mac)**

The code is **completely portable**! Just 3 commands:

```bash
# 1. Clone repo
git clone https://github.com/gourab-jonty/AI-project.git
cd AI-project

# 2. Setup (one-time)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py index      # Index your files

# 3. Run
python main.py            # Interactive mode
```

**That's it!** Setup takes 5-10 minutes on most machines.

---

## 🛠️ Installation by OS

### **Linux/Mac**
```bash
git clone https://github.com/gourab-jonty/AI-project.git
cd AI-project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

### **Windows (PowerShell)**
```powershell
git clone https://github.com/gourab-jonty/AI-project.git
cd AI-project
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## 💬 Usage

### Interactive Mode
```bash
python main.py

You: What Python files do I have?
Jonty: I found these in your directory...

You: Calculate 2 + 2 * 3
Jonty: 2 + 2 * 3 = 8

You: quit
```

### Single Query
```bash
python main.py "Search for PDFs about machine learning"
```

### Index Files
```bash
python main.py index
```

### Run Tests
```bash
python test_integration.py
```

---

## 🛠️ Available Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `calculator` | Math expressions | `2 + 2 * 3` |
| `open_file` | Open files | `open ~/file.pdf` |
| `open_app` | Launch apps | `open firefox` |
| `search_files` | Find files | `find *.pdf` |
| `read_file` | Read file content | `show ~/file.txt` |
| `get_time` | Current time | `what time is it` |
| `get_date` | Current date | `what's today` |
| `set_alarm` | Set alarm | `alarm at 3 PM` |
| `list_directory` | Browse folders | `list ~/Documents` |

---

## 🚀 Multi-Machine Setup (Fast!)

### **Setup on Windows with Higher Config**

Since code is only 50MB, setup is **fast everywhere**:

```powershell
# 1. Clone
git clone https://github.com/gourab-jonty/AI-project.git
cd AI-project

# 2. Setup
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# 3. Download Model (one-time)
cd models
# Download TinyLlama or use Ollama
cd ..

# 4. Run
python main.py
```

**Timeline:**
- Clone: 1 min
- Venv + dependencies: 3-5 mins (faster with good internet)
- Model download: 2-3 mins (638MB)
- Total: **~10 minutes**

### **Setup on Mac**

```bash
git clone https://github.com/gourab-jonty/AI-project.git
cd AI-project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

---

## 🔄 Phases Overview

### ✅ Phase 1: Data Engine
- File loader & chunker
- Embeddings (FAISS)
- RAG retrieval
- Status: **COMPLETE**

### ✅ Phase 2: AI Brain
- LLM integration
- Model loading (TinyLlama)
- Prompt system
- Status: **COMPLETE**

### ✅ Phase 3: Tools
- Calculator
- Alarms
- File operations
- Status: **COMPLETE**

### ✅ Phase 4: Agent
- Intent detection
- Smart routing
- Status: **COMPLETE**

### 🏗️ Phase 5: UI
- Streamlit interface
- Status: **IN PROGRESS**

### 🏗️ Phase 6: Upgrades
- LLaMA 3 (GPU)
- Whisper (audio)
- Vision models
- Status: **PLANNED**

---

## � Project Structure

```
jonty/
├── agent/                    # Core agent components
│   ├── brain.py             # LLM interface  
│   ├── tools.py             # Action system
│   ├── router.py            # Decision engine
│   ├── loader.py            # File loading
│   ├── chunker.py           # Text chunking
│   ├── embedder.py          # Text embeddings
│   ├── retriever.py         # File search
│   └── vector_db.py         # Vector storage
├── main.py                  # Main entry point
├── indexer.py              # File indexing
├── config.yaml             # Configuration
├── requirements.txt        # Dependencies (clean, portable)
├── test_integration.py     # Integration tests
└── SETUP_GUIDE.md          # Detailed setup guide

[GIT IGNORED - Not Committed]:
├── venv/                   # Python environment (~23MB)
├── models/                 # LLM model (~638MB, only downloaded once)
├── vector_db/              # Indexed files (generated, regenerable)
└── logs/                   # Logs (generated on run)
```

## 💾 What's Ignored (Not in Git)

To keep the repo lightweight (~50MB), these are excluded:

| Folder | Size | Why Ignored | Regenerates? |
|--------|------|-------------|--------------|
| `venv/` | ~23MB | Per-machine environment | ✅ Yes (venv setup) |
| `models/` | ~638MB | LLM model (download once) | ✅ Yes (wget) |
| `vector_db/` | Variable | Generated from your files | ✅ Yes (run index) |
| `logs/` | Small | Auto-generated logs | ✅ Yes (on run) |

**Result:** 
- Git repo: **~50MB** (includes all code)
- Full setup: **~750MB** (with all components)

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
