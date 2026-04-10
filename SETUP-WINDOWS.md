# 🪟 JONTY SETUP FOR WINDOWS (High-End Systems)

## ⚡ FASTEST SETUP (2 Minutes)

### **Option 1: Using Ollama (Recommended - Automatic Model Management)**

```powershell
# 1. Download Ollama
# Go to: https://ollama.ai
# Download and install (auto-configures NVIDIA/AMD GPU if available)

# 2. Pull latest LLaMA 3 model
ollama pull llama3

# 3. Keep Ollama running (open separate PowerShell)
ollama serve

# 4. In new PowerShell, clone Jonty
git clone https://github.com/gourab-jonty/AI-project.git
cd AI-project

# 5. Setup Jonty
python setup.py

# 6. Update config
# Edit config.yaml:
# - Change: backend: "ollama"
# - Change: model_name: "llama3"

# 7. Run
python main.py
```

**Done!** Ollama handles all models automatically.

---

### **Option 2: Using llama-cpp (Manual Model Download)**

```powershell
# If you want more control, download model manually:

# 1. Clone Jonty
git clone https://github.com/gourab-jonty/AI-project.git
cd AI-project

# 2. Setup environment
python setup.py

# 3. Create models folder
mkdir models
cd models

# 4. Download LLaMA 3 (8B, ~5GB)
# Go to: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF
# Download: llama-2-7b-chat.Q5_K_M.gguf
# Or use PowerShell Invoke-WebRequest to download

cd ..

# 5. Update config
# Edit config.yaml:
# - Change: backend: "llama-cpp"
# - Change: model_path: "models/llama-2-7b-chat.Q5_K_M.gguf"

# 6. Run
python main.py
```

---

## 🎯 MODEL OPTIONS FOR WINDOWS (High-End)

| Model | Size | Quality | Speed | RAM Needed |
|-------|------|---------|-------|-----------|
| **llama3** | 8B | ⭐⭐⭐⭐⭐ Best | ~20s | 16GB+  |
| **mistral** | 7B | ⭐⭐⭐⭐ Great | ~10s | 12GB+ |
| **neural-chat** | 7B | ⭐⭐⭐⭐ Good | ~12s | 12GB+ |
| **dolphin-mixtral** | 7B | ⭐⭐⭐⭐ Good | ~15s | 14GB+ |
| **tinyllama** | 1.1B | ⭐⭐ Basic | ~2s | 4GB  |

---

## 💻 GPU ACCELERATION (Optional but Recommended)

### **NVIDIA GPU (CUDA)**

```powershell
# 1. Check GPU
nvidia-smi

# 2. Install CUDA toolkit (if not already)
# Download from: https://developer.nvidia.com/cuda-downloads

# 3. Install GPU-accelerated libraries
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 4. Verify GPU is detected
python -c "import torch; print(torch.cuda.is_available())"
# Should print: True
```

### **AMD GPU (ROCm)**

```powershell
# Install AMD ROCm support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.7
```

**With GPU:** Responses ~10x faster!

---

## 🚀 STEP-BY-STEP SETUP

### **For Complete Beginners:**

1. **Install Python 3.10+**
   - Download: https://python.org
   - During install, check ✅ "Add Python to PATH"

2. **Install Ollama (Easiest)**
   - Download: https://ollama.ai
   - Install
   - Run → keep open

3. **Clone Jonty**
   ```powershell
   git clone https://github.com/gourab-jonty/AI-project.git
   cd AI-project
   ```

4. **Setup (Automated)**
   ```powershell
   python setup.py
   # Follow prompts - auto-downloads everything
   ```

5. **Configure**
   ```powershell
   # Edit config.yaml (open with Notepad)
   # Find: backend: "llama-cpp"
   # Change to: backend: "ollama"
   # Find: model_name: "tinyllama"
   # Change to: model_name: "llama3"
   ```

6. **Index Your Files**
   ```powershell
   python main.py index
   # Wait for completion...
   ```

7. **Start Using**
   ```powershell
   python main.py
   # Interactive chat starts!
   ```

---

## 📊 EXPECTED PERFORMANCE

| System | Model  | Response Time |
|--------|--------|-------------|
| i7 16GB | LLaMA 3 | 15-25s |
| i9 32GB | LLaMA 3 | 8-12s |
| i9 + RTX 3080 | LLaMA 3 | 2-3s |
| i9 + RTX 4090 | LLaMA 3 | 0.5-1s |

---

## 🔧 TROUBLESHOOTING

### "Python not found"
- Install from https://python.org
- Restart PowerShell after install
- Run: `python --version`

### "Ollama not connecting"
- Ensure `ollama serve` is running
- Check: `ollama list` (shows downloaded models)
- Restart Ollama

### "Out of memory"
Edit `config.yaml`:
```yaml
model:
  max_tokens: 512    # Reduce from 1024
  temperature: 0.5   # Lower creativity
```

### "Slow performance"
- First query loads model (normal)
- Subsequent queries faster
- Enable GPU for 10x speedup
- Or use smaller model (mistral instead of llama3)

### "Can't download model"
- Check internet connection
- Try Ollama method (it downloads automatically)
- Manual download: Click link, save to `models/` folder

---

## ✅ VERIFY SETUP

Test everything works:

```powershell
# 1. Check Python
python --version          # Should be 3.10+

# 2. Check imports
python -c "import faiss, torch; print('✅ OK')"

# 3. Check Ollama models
ollama list               # See installed models

# 4. Run test query
python main.py "hello"    # Simple test

# 5. Run full integration tests
python test_integration.py
```

---

## 🎯 RECOMMENDED SETUP FOR YOU

Based on "High-End Windows System":

1. **Use Ollama** (automatic, no manual downloads)
2. **Choose llama3** (best quality for your system)
3. **Enable GPU** if you have NVIDIA/AMD
4. **Increase max_tokens to 1024** (better responses)

```yaml
# In config.yaml
model:
  backend: "ollama"
  ollama:
    model_name: "llama3"

performance:
  use_gpu: true
  device: "cuda"    # If NVIDIA
```

---

## 🚀 READY?

```powershell
# Copy-paste this one command:
$url = "https://ollama.ai/"; Start-Process $url; Write-Host "Download Ollama, install, then run setup.py"
```

**Questions?** Check `DEPLOYMENT.md` or `README.md`

**Happy Jontying!** 🚀
