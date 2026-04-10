# 📦 JONTY INSTALLATION GUIDE
## Choose Your Setup Method

---

## ⚡ QUICKEST METHOD (Recommended)

### **Windows**
```powershell
git clone https://github.com/gourab-jonty/AI-project.git
cd AI-project
python setup.py
```

### **Linux/Mac**
```bash
git clone https://github.com/gourab-jonty/AI-project.git
cd AI-project
chmod +x setup.sh
./setup.sh
```

**Done!** The script handles everything automatically.

---

## 🎯 WHAT EACH SCRIPT DOES

| Script | OS | What It Does |
|--------|-----|-----------|
| `setup.py` | All | ✅ Interactive, cross-platform, handles everything |
| `setup.sh` | Linux/Mac | ✅ Automated, fastest for Unix systems |
| `setup.bat` | Windows | ✅ Batch file alternative for Windows |
| `DEPLOYMENT.md` | All | 📖 Manual step-by-step guide |

---

## 📋 SETUP CHECKLIST

After running any setup script, you should have:

```
✅ Virtual environment created (venv/)
✅ Dependencies installed (pip packages)
✅ Directories created (models/, logs/, vector_db/)
✅ Model downloaded (optional, ~/1.1GB)
✅ Config file ready (config.yaml)
```

Verify:
```bash
# Check directory structure
ls -la
# Should see: agent/, config.yaml, main.py, venv/, etc.

# Activate venv and test
source venv/bin/activate  # or: venv\Scripts\activate on Windows
python -c "import faiss, torch; print('✅ OK')"
```

---

## 🚀 FIRST RUN

### **1. Configure Your Paths**
```bash
nano config.yaml
# Or edit with your favorite editor

# Update the 'paths' section:
paths:
  - ~/Documents
  - ~/Downloads
  - ~/Desktop
```

### **2. Index Your Files**
```bash
python main.py index
# This scans all files and creates vector embeddings
# First time: 5-30 minutes depending on file count
```

### **3. Start Using**
```bash
python main.py
# Interactive mode - ask questions about your files!
```

---

## 🔧 TROUBLESHOOTING

### Setup Script Fails

**Python not found:**
```bash
# Install Python 3.10+
# Download from: python.org
# Mac: brew install python@3.11
# Linux: apt-get install python3
```

**Permission denied on scripts:**
```bash
chmod +x setup.sh   # Linux/Mac
```

**Model download fails:**
- Run script again to retry
- Or manually download from: https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF

### After Setup

**"Module not found" error:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Low disk space:**
Skip model download during setup
Or use Ollama instead (it manages its own storage)

---

## 📊 SETUP TIME EXPECTATIONS

| Machine | Time |
|---------|------|
| Fast internet (100 Mbps) | 5-10 min |
| Slower internet (10 Mbps) | 15-20 min |
| Very slow (1 Mbps) | 50+ min |
| Without model download | 2-3 min |

---

## 🎯 CHOOSE YOUR PATH

### **I'm on Windows**
→ Run `python setup.py`

### **I'm on Mac/Linux**
→ Run `chmod +x setup.sh && ./setup.sh`

### **I want manual control**
→ See `DEPLOYMENT.md` for step-by-step

### **I want to use Ollama (no downloads)**
→ See `DEPLOYMENT.md` - "LLM Backend Options"

---

## ✅ Everything Installed?

Test it:
```bash
python main.py
# Should show: 🤖 Starting Jonty AI Assistant...
# Then: You: (waiting for input)
```

Try a query:
```
You: what time is it
Jonty: Current time is...
```

---

## 🚀 NEXT STEPS

1. ✅ Setup complete
2. ✅ Files indexed
3. ⏭️ Start asking questions!

Try these queries:
- "What Python files do I have?"
- "Calculate 2 + 2 * 3"
- "List my documents"
- "Set an alarm for 3 PM"

---

## 📖 NEED MORE HELP?

- **Setup issues?** → `DEPLOYMENT.md`
- **How to use?** → `SETUP_GUIDE.md`
- **Overview?** → `README.md`
- **GitHub?** → https://github.com/gourab-jonty/AI-project

---

**Happy Jontying! 🚀**
