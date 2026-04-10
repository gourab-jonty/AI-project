# 🐧 JONTY SETUP FOR LINUX (High-End Systems)

## ⚡ FASTEST SETUP (2 Minutes)

### **Option 1: Using Ollama (Recommended - Automatic Model Management)**

```bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Pull latest LLaMA 3 model
ollama pull llama3

# 3. Start Ollama in background
ollama serve &

# 4. Clone Jonty
git clone https://github.com/gourab-jonty/AI-project.git
cd AI-project

# 5. Setup
chmod +x setup.sh
./setup.sh

# 6. Update config
# Edit config.yaml:
# - backend: "ollama"
# - model_name: "llama3"

# 7. Run
python main.py
```

**Done!** Ollama handles everything automatically.

---

### **Option 2: Using llama-cpp (Manual Control)**

```bash
# 1. Clone
git clone https://github.com/gourab-jonty/AI-project.git
cd AI-project

# 2. Setup environment
python3 -m venv venv
source venv/bin/activate

# 3. Install with GPU support
pip install -r requirements.txt
pip install llama-cpp-python --force-reinstall --no-cache-dir

# 4. Download model
mkdir -p models
cd models

# Option A: Download LLaMA 3 (8B, ~5GB)
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_M.gguf

# Option B: Mistral 7B (faster, ~4GB)
# wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q5_K_M.gguf

cd ..

# 5. Update config
nano config.yaml
# Find and change:
# backend: "llama-cpp"
# model_path: "models/llama-2-7b-chat.Q5_K_M.gguf"

# 6. Index files
python3 main.py index

# 7. Run
python3 main.py
```

---

## 🎯 MODEL OPTIONS FOR LINUX (High-End)

| Model | Size | Quality | Speed | RAM | GPU |
|-------|------|---------|-------|-----|-----|
| **llama3** | 8B | ⭐⭐⭐⭐⭐ | ~20s | 16GB | ~8GB |
| **mistral** | 7B | ⭐⭐⭐⭐ | ~10s | 12GB | ~7GB |
| **neural-chat** | 7B | ⭐⭐⭐⭐ | ~12s | 12GB | ~7GB |
| **dolphin-mixtral** | 7B | ⭐⭐⭐⭐ | ~15s | 14GB | ~7GB |
| **tinyllama** | 1.1B | ⭐⭐ | ~2s | 4GB | ~1GB |

---

## 💻 GPU ACCELERATION (Recommended for High-End)

### **NVIDIA GPU (CUDA)**

```bash
# 1. Check GPU
nvidia-smi

# 2. Install CUDA Toolkit
# Ubuntu:
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2104/x86_64/cuda-repo-ubuntu2104_11.7.1-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2104_11.7.1-1_amd64.deb
sudo apt-get -y install cuda

# 3. Install GPU PyTorch
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 4. Verify GPU
python3 -c "import torch; print(torch.cuda.is_available())"
# Should print: True
```

### **AMD GPU (ROCm)**

```bash
# Install ROCm
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.7

# Verify
python3 -c "import torch; print(torch.cuda.is_available())"
```

### **Intel GPU (oneAPI)**

```bash
# Install Intel GPU support
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/xpu
```

**With GPU:** Responses 5-10x faster!

---

## 🚀 STEP-BY-STEP SETUP (Ubuntu/Debian)

### **1. Prerequisites**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3 python3-venv python3-dev git build-essential

# Verify Python 3.10+
python3 --version
```

### **2. Clone Jonty**

```bash
git clone https://github.com/gourab-jonty/AI-project.git
cd AI-project
```

### **3. Create Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

### **4. Install Dependencies**

```bash
# Basic installation
pip install -r requirements.txt

# With GPU support (NVIDIA)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### **5. Download Model (Optional if using Ollama)**

```bash
# Using Ollama (recommended):
ollama pull llama3

# OR manually download:
mkdir -p models
cd models
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_M.gguf
cd ..
```

### **6. Configure**

```bash
# Copy high-end config
cp config-highend.yaml config.yaml

# Or edit manually
nano config.yaml
# Set: backend: "ollama" or "llama-cpp"
# Set: model_name: "llama3"
```

### **7. Index Your Files**

```bash
python3 main.py index
# Wait for completion (5-30 min depending on file count)
```

### **8. Start Using**

```bash
python3 main.py
# You: hello
# Jonty: Hello! How can I help you today?
```

---

## 📊 EXPECTED PERFORMANCE

| CPU | RAM | GPU | Model | Response |
|-----|-----|-----|-------|----------|
| Ryzen 7 | 16GB | None | LLaMA 3 | 15-25s |
| Ryzen 9 | 32GB | None | LLaMA 3 | 8-12s |
| i9 | 32GB | RTX 3090 | LLaMA 3 | 2-3s |
| i9 | 64GB | RTX 4090 | LLaMA 3 | 0.5-1s |

---

## 🔧 TROUBLESHOOTING

### "ModuleNotFoundError"
```bash
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

### "Ollama not found"
```bash
# Reinstall Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Or start manually
ollama serve
```

### "CUDA not found"
```bash
# Check installation
nvidia-smi   # Should show GPU info

# Reinstall CUDA PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 --force-reinstall
```

### "Out of memory"
Edit `config.yaml`:
```yaml
model:
  max_tokens: 512      # Reduce from 1024
  temperature: 0.5
  llama_cpp:
    gpu_layers: 10     # Reduce GPU layers
```

### "Slow on first query"
- Normal (model loads into memory)
- Subsequent queries much faster
- Use GPU to speed up

---

## ✅ VERIFY SETUP

```bash
# 1. Activate venv
source venv/bin/activate

# 2. Check Python
python3 --version          # 3.10+

# 3. Check imports
python3 -c "import faiss, torch; print('✅ OK')"

# 4. Check GPU
nvidia-smi                 # GPU status

# 5. Check Ollama models
ollama list

# 6. Test query
python3 main.py "hello"

# 7. Full tests
python3 test_integration.py
```

---

## 🎯 RECOMMENDED CONFIG FOR HIGH-END LINUX

Create/Edit `config.yaml`:

```yaml
model:
  backend: "ollama"           # Auto-managed models
  ollama:
    model_name: "llama3"      # Best quality
    keep_alive: "5m"

performance:
  use_gpu: true
  device: "cuda"              # NVIDIA
  cpu_threads: 32             # High core count
  enable_cache: true
  cache_size_mb: 4096

embedding:
  model_name: "sentence-transformers/all-mpnet-base-v2"
  batch_size: 256             # High batch for GPU
  device: "cuda"

vector_db:
  chunk_size: 1024            # Larger chunks
  overlap: 100
```

---

## 🚀 ONE-LINER SETUP (Ubuntu)

```bash
curl -fsSL https://ollama.ai/install.sh | sh && \
git clone https://github.com/gourab-jonty/AI-project.git && \
cd AI-project && \
python3 -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt && \
echo "✅ Setup complete! Run: python3 main.py"
```

---

## 📚 COMMON WORKFLOWS

### **Daily Use**
```bash
cd /path/to/AI-project
source venv/bin/activate
python3 main.py
```

### **Re-index Files**
```bash
python3 main.py index
```

### **Check GPU Usage During Query**
```bash
# In another terminal
watch nvidia-smi
```

### **Run Background Service**
```bash
nohup python3 main.py > jonty.log 2>&1 &
tail -f jonty.log
```

---

## 🎓 TIPS FOR LINUX

- **Systemd Service:** Create `/etc/systemd/system/jonty.service` for auto-start
- **Cron Jobs:** Schedule `python3 main.py index` weekly  
- **Docker:** Build containers for reproducible setup
- **SSH Tunneling:** Access from remote machines

---

**Happy Jontying on Linux!** 🐧🚀
