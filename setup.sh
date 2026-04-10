#!/bin/bash
# Jonty - Automated Setup Script for Linux/Mac
# Usage: chmod +x setup.sh && ./setup.sh

set -e  # Exit on error

echo "🚀 Jonty Setup Automation"
echo "=========================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python: $python_version"

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ venv created${NC}"
else
    echo -e "${GREEN}✓ venv already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Create directories
echo -e "${YELLOW}Creating necessary directories...${NC}"
mkdir -p models logs vector_db
echo -e "${GREEN}✓ Directories created${NC}"

# Download model (optional)
read -p "Download TinyLlama model? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Downloading TinyLlama model (~1.1GB)...${NC}"
    cd models
    if [ ! -f "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf" ]; then
        wget -q --show-progress https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
        echo -e "${GREEN}✓ Model downloaded${NC}"
    else
        echo -e "${GREEN}✓ Model already exists${NC}"
    fi
    cd ..
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Configure your file paths in config.yaml"
echo "2. Run: python main.py index   (to index your files)"
echo "3. Run: python main.py         (start interactive mode)"
echo ""
