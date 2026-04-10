# 🤖 Jonty - Personal AI Assistant
# Complete Setup & Usage Guide

## What is Jonty?

Jonty is a **full-stack offline personal AI assistant** that:
- 🔍 Searches your local files (PDFs, documents, code)
- 🧠 Understands and answers using offline LLM
- 🧰 Performs actions (calculate, open files, etc.)
- 💾 Remembers conversation context
- 🔒 100% offline - nothing leaves your computer

---

## ⚡ Quick Setup (5 mins)

### Step 1: Install Dependencies
```bash
cd /home/gourab-nandi/AI/jonty
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Choose LLM Backend

**Option A: Ollama (Easiest)**
1. Download: https://ollama.ai
2. Run: `ollama pull tinyllama && ollama serve`
3. Keep running in background!

**Option B: llama-cpp-python**
```bash
pip install llama-cpp-python
mkdir models && cd models
wget https://... tinyllama.gguf
cd ..
```

### Step 3: Configure
Edit `config.yaml` - set your file paths:
```yaml
paths:
  - ~/Documents
  - ~/Downloads
  - ~/Desktop
```

### Step 4: Index Your Files
```bash
python main.py index
```

### Step 5: Start Using
```bash
python main.py    # Interactive mode
```

---

## 💬 How to Use

### Interactive Mode
```bash
python main.py

You: What Python files do I have?
Jonty: I found these Python files in your Documents...

You: Calculate 2 + 2 * 3  
Jonty: 2 + 2 * 3 = 8

You: Set an alarm for 3 PM
Jonty: ✓ Alarm set for 15:00

You: quit
```

### Single Query
```bash
python main.py "Search my documents for Python tutorials"
```

### Commands
```bash
Commands in interactive mode:
  type 'help'   - Show available commands
  type 'memory' - Conversation history
  type 'index'  - Re-index files
  type 'quit'   - Exit
```

---

## 🛠️ Available Tools

### Information Tools
- `get_time()` - Current time
- `get_date()` - Current date

### Action Tools  
- `calculate()` - Math expressions
- `open_file()` - Open any file
- `open_app()` - Launch applications
- `set_alarm()` - Schedule alerts

### File Tools
- `search_files()` - Find files by pattern
- `read_file()` - Read file contents
- `list_directory()` - Browse folders

---

## 📊 Architecture Overview

### Phase 1: Data Engine ✅
- **Indexer**: Scans files
- **Loader**: Extracts text (PDF, TXT, DOCX, etc.)
- **Chunker**: Splits text smartly
- **Embedder**: Converts to vectors
- **Vector DB**: FAISS storage
- **Retriever**: Semantic search

### Phase 2: Brain ✅
- **Brain Module**: LLM interface
- Supports: Ollama, llama-cpp-python
- TinyLlama (1.1B) for CPU
- LLaMA 3 (future GPU upgrade)

### Phase 3: Tools ✅
- **Tools Module**: Action system
- 9+ tools built-in
- Extensible design

### Phase 4: Agent ✅
- **Router**: Decision making
- Chooses: Search? Tools? Answer?
- Memory management
- Context building

---

## 🔍 File Types Supported

| Type | Status | Method |
|------|--------|--------|
| PDF | ✅ | PyMuPDF |
| TXT/Code | ✅ | Direct read |
| DOCX | ✅ | python-docx |
| XLSX | ✅ | pandas |
| Images | ⚠️ | OCR (optional) |
| Audio | 🏗️ | Whisper (future) |

---

## ⚙️ Configuration Reference  

```yaml
# config.yaml

# Paths to index (add your folders)
paths:
  - ~/Documents
  - ~/Downloads  
  - ~/Desktop
  - ~/Projects

# LLM Model Settings
model_name: tinyllama          # or: llama3, mistral
model_path: ~/models/tinyllama.gguf
max_tokens: 512               # Response length
temperature: 0.7              # Creativity (0-1)
top_k: 40                     # Top K sampling
top_p: 0.95                   # Nucleus sampling

# Embedding Model
embed_model: sentence-transformers/all-MiniLM-L6-v2

# Chunking
chunk_size: 500               # Characters per chunk
chunk_overlap: 50             # Overlap between chunks

# Vector DB
vector_db_path: ./vector_db
```

---

## 🐛 Troubleshooting

### "Model not loaded"
- For Ollama: Make sure `ollama serve` is running
- For llama-cpp: Check model file exists at path

### "Out of memory"
- Reduce `chunk_size` to 250
- Reduce `max_tokens` to 256
- Close other applications

### "No files indexed"  
- Run: `python main.py index`
- Check paths in config.yaml

### "Slow performance"
- First indexes are slow (normal)
- Subsequent queries much faster
- Consider GPU for next phase

---

## 🧪 Testing

Run all integration tests:
```bash
python test_integration.py
```

Tests:
- Phase 1: RAG system
- Phase 2: Brain system
- Phase 3: Tools system  
- Phase 4: Agent system

---

## 📁 Project Structure

```
jonty/
├── agent/
│   ├── brain.py          # LLM inference
│   ├── tools.py          # 9+ action tools
│   ├── router.py         # Decision engine
│   ├── loader.py         # PDF/DOC loading
│   ├── chunker.py        # Text splitting
│   ├── embedder.py       # Text→vectors
│   ├── retriever.py      # Search
│   └── vector_db.py      # FAISS storage
├── main.py               # Entry point
├── indexer.py            # File indexing
├── config.yaml           # Configuration
├── requirements.txt      # Dependencies
├── test_integration.py   # Tests
└── vector_db/            # Indexed data
```

---

## 🚀 Next Steps

1. **Personalize**: Add your file paths to `config.yaml`
2. **Index**: Run `python main.py index`
3. **Query**: Try interactive mode
4. **Extend**: Add custom tools in `agent/tools.py`

---

## 💡 Tips & Tricks

- **Privacy**: All data stays local, no cloud required
- **GPU Mode**: Future phase for faster inference
- **Persistence**: Vector DB saves between sessions
- **Memory**: Jonty remembers last 10 exchanges
- **Extensible**: Easy to add new tools

---

## 📊 Performance Expectations

| Operation | Time | Hardware |
|-----------|------|----------|
| Index 100 files | 5-30 min | Any CPU |
| First query | 10-30 sec | 4-core CPU |
| Subsequent queries | 2-5 sec | 4-core CPU |
| With GPU | 0.5-2 sec | NVIDIA GPU |

---

## 🔗 Resources

- **Ollama**: https://ollama.ai
- **FAISS**: https://github.com/facebookresearch/faiss
- **Sentence Transformers**: huggingface.co/sentence-transformers
- **TinyLlama**: huggingface.co/PY007/TinyLlama-1.1B

---

**Happy Jontying! 🚀**
