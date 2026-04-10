# 🚀 JONTY DEPLOYMENT GUIDE
## One-Command Setup on Any Machine

This guide helps you quickly deploy Jonty on **Windows, Mac, or Linux** with higher specs.

---

## ⚡ FASTEST SETUP (3 Steps)

### **Step 1: Clone Repository**
```bash
git clone https://github.com/gourab-jonty/AI-project.git
cd AI-project
```

### **Step 2: Auto-Setup (Run Once)**

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows PowerShell:**
```powershell
python setup.py
```

### **Step 3: Start Using**
```bash
python main.py
```

---

## 🖥️ MANUAL SETUP BY OS

### **Windows (PowerShell)**

```powershell
# 1. Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# Optional: Install GPU support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 3. Download model (optional, uses llama-cpp)
mkdir models
cd models
# Download from: https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF
# Or use Ollama instead
cd ..

# 4. Index your files
python main.py index

# 5. Run
python main.py
```

### **Linux (Ubuntu/Debian)**

```bash
# 1. Ensure Python 3.10+ and git
sudo apt-get update
sudo apt-get install python3 python3-venv git

# 2. Clone and setup
git clone https://github.com/gourab-jonty/AI-project.git
cd AI-project

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# Optional: GPU support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 5. Download model or use Ollama
# See "LLM Backend" section below

# 6. Run
python3 main.py
```

### **Mac (Intel/Apple Silicon)**

```bash
# 1. Ensure Homebrew is installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install Python
brew install python@3.11

# 3. Clone and setup
git clone https://github.com/gourab-jonty/AI-project.git
cd AI-project

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# For Apple Silicon GPU acceleration:
pip install -e . --no-build-isolation

# 6. Run
python3 main.py
```

---

## 🧠 LLM BACKEND OPTIONS

### **Option A: Ollama (Recommended - Easiest)**

**All Platforms:**
1. Download from: https://ollama.ai
2. Install and run:
```bash
ollama pull tinyllama
ollama serve  # Keep running in background
```

**Update config.yaml:**
```yaml
model:
  name: "TinyLlama"
  backend: "ollama"  # Add this line
```

### **Option B: llama-cpp-python (More Control)**

**All Platforms:**
```bash
# Install
pip install llama-cpp-python

# Download model to models/ folder
cd models
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
cd ..
```

**Update config.yaml:**
```yaml
model:
  name: "TinyLlama"
  model_path: "models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
  backend: "llama-cpp"  # Add this line
```

---

## 🚀 GPU ACCELERATION (Optional - Higher Config Machines)

### **NVIDIA GPU (CUDA)**

```bash
# Install GPU-accelerated PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For llama-cpp with CUDA:
pip install llama-cpp-python --force-reinstall --no-cache-dir
```

### **AMD GPU (ROCm)**

```bash
# Install ROCm version
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.7
```

### **Mac GPU (Metal)**

```bash
# Metal support is built-in with latest PyTorch
pip install torch torchvision torchaudio
```

---

## ✅ VERIFICATION CHECKLIST

After setup, verify everything works:

```bash
# 1. Check Python version
python --version  # Should be 3.10+

# 2. Test imports
python -c "import faiss; import torch; print('✅ All imports OK')"

# 3. Check model
ls -lh models/
# Should show tinyllama model if using llama-cpp

# 4. Test LLM
python -c "from agent.brain import Brain; b = Brain({'model_name': 'tinyllama'}); print(b.load_model())"

# 5. Run integration tests
python test_integration.py
```

---

## 📊 EXPECTED PERFORMANCE

| Machine | CPU/GPU | Setup Time | Query Time |
|---------|---------|-----------|-----------|
| Old Laptop (4-core CPU) | Any | 10 min | 3-5 sec |
| Modern Laptop (8-core) | Any | 5 min | 1-2 sec |
| Server (16-core) | Any | 3 min | <1 sec |
| With GPU (NVIDIA)| RTX 3080 | 3 min | 0.3 sec |
| With GPU (RTX 4090) | RTX 4090 | 3 min | 0.1 sec |

---

## 🐛 TROUBLESHOOTING

### "Import Error: No module named 'faiss'"
```bash
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

### "Model not found"
```bash
# Verify you downloaded or Ollama is running
ollama serve  # for Ollama
# or
ls models/tinyllama*  # for llama-cpp
```

### "Out of memory"
Reduce in config.yaml:
```yaml
model:
  max_tokens: 256  # Lower from 512
embedding:
  batch_size: 32   # Lower from 64
```

### "Slow performance"
- First query is slow (model loading) - normal
- Use GPU version for faster inference
- Reduce chunk_size in config.yaml

---

## 📦 MINIMAL vs FULL INSTALL

### **Minimal (~200MB)**
```bash
# Skip heavy dependencies
pip install faiss-cpu sentence-transformers pyyaml
# Manual model download only
```

### **Full (With GPU)**
```bash
pip install -r requirements.txt
pip install torch  # Choose GPU-enabled version
pip install llama-cpp-python  # GPU support
```

---

## 🔄 UPDATING CODE

Get latest updates:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
python main.py index  # Re-index if needed
```

---

## 📱 DEPLOYMENT OPTIONS

### **Local Machine**
```bash
python main.py  # Interactive CLI
```

### **Remote Server (SSH)**
```bash
# On server:
nohup python main.py > jonty.log 2>&1 &

# Check status:
tail -f jonty.log
```

### **Docker (Future)**
```bash
docker build -t jonty .
docker run -it jonty
```

### **Cloud (AWS/GCP/Azure - Future)**
- Containerize with Docker
- Deploy on cloud VM or serverless

---

## 🎯 NEXT STEPS

1. ✅ Clone repository
2. ✅ Run setup script
3. ✅ Choose LLM backend (Ollama recommended)
4. ✅ Index your files
5. ✅ Start using!

---

**Any issues? Check logs:**
```bash
tail -f logs/jonty.log
```

**Questions?** Open issue on GitHub!
