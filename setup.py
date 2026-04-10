#!/usr/bin/env python3
"""
Jonty - Cross-Platform Setup Script
Works on Windows, Mac, and Linux
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class JontySetup:
    def __init__(self):
        self.os_type = platform.system()
        self.project_dir = Path(__file__).parent
        self.colors = {
            'GREEN': '\033[92m',
            'YELLOW': '\033[93m',
            'RED': '\033[91m',
            'END': '\033[0m'
        }
    
    def log(self, message, level='INFO'):
        """Print colored log message"""
        if self.os_type == 'Windows':
            # No colors on Windows
            print(f"[{level}] {message}")
        else:
            color = {
                'INFO': self.colors['YELLOW'],
                'OK': self.colors['GREEN'],
                'ERROR': self.colors['RED']
            }.get(level, self.colors['END'])
            print(f"{color}[{level}] {message}{self.colors['END']}")
    
    def run_command(self, command, description=""):
        """Run shell command"""
        if description:
            self.log(description)
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=str(self.project_dir),
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                self.log(f"Error: {result.stderr}", 'ERROR')
                return False
            return True
        except Exception as e:
            self.log(f"Command failed: {e}", 'ERROR')
            return False
    
    def check_python(self):
        """Check Python version"""
        self.log(f"Python version: {sys.version}", 'INFO')
        version_info = sys.version_info
        
        if version_info.major < 3 or version_info.minor < 10:
            self.log("Python 3.10+ required", 'ERROR')
            return False
        
        self.log("Python version OK", 'OK')
        return True
    
    def create_venv(self):
        """Create virtual environment"""
        venv_path = self.project_dir / 'venv'
        
        if venv_path.exists():
            self.log("Virtual environment already exists", 'OK')
            return True
        
        self.log("Creating virtual environment", 'INFO')
        
        if self.os_type == 'Windows':
            cmd = f"{sys.executable} -m venv venv"
        else:
            cmd = f"{sys.executable} -m venv venv"
        
        return self.run_command(cmd)
    
    def install_dependencies(self):
        """Install Python dependencies"""
        self.log("Installing dependencies", 'INFO')
        
        if self.os_type == 'Windows':
            pip_cmd = 'venv\\Scripts\\pip'
        else:
            pip_cmd = 'venv/bin/pip'
        
        # Upgrade pip
        self.run_command(f"{pip_cmd} install --upgrade pip setuptools wheel")
        
        # Install requirements
        return self.run_command(f"{pip_cmd} install -r requirements.txt")
    
    def create_directories(self):
        """Create necessary directories"""
        self.log("Creating directories", 'INFO')
        
        dirs = ['models', 'logs', 'vector_db']
        for dir_name in dirs:
            dir_path = self.project_dir / dir_name
            dir_path.mkdir(exist_ok=True)
        
        self.log("Directories created", 'OK')
        return True
    
    def download_model(self, force=False):
        """Download TinyLlama model"""
        model_path = self.project_dir / 'models' / 'tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf'
        
        if model_path.exists() and not force:
            self.log("Model already exists", 'OK')
            return True
        
        self.log("Would you like to download TinyLlama (~1.1GB)? (y/n): ", 'INFO')
        response = input().lower()
        
        if response != 'y':
            self.log("Skipping model download", 'INFO')
            return True
        
        self.log("Downloading model (this may take 2-5 minutes)", 'INFO')
        
        url = "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
        
        try:
            import urllib.request
            urllib.request.urlretrieve(url, str(model_path))
            self.log(f"Model downloaded to {model_path}", 'OK')
            return True
        except Exception as e:
            self.log(f"Download failed: {e}", 'ERROR')
            self.log("You can download manually from: " + url)
            return False
    
    def run(self):
        """Run complete setup"""
        print("\n" + "="*50)
        print("  Jonty - Automated Setup")
        print("="*50 + "\n")
        
        steps = [
            ("Checking Python version", self.check_python),
            ("Creating virtual environment", self.create_venv),
            ("Installing dependencies", self.install_dependencies),
            ("Creating directories", self.create_directories),
            ("Downloading model", self.download_model),
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                self.log(f"Setup failed at: {step_name}", 'ERROR')
                return False
        
        print("\n" + "="*50)
        self.log("Setup Complete!", 'OK')
        print("="*50 + "\n")
        
        print("Next steps:")
        print("1. Edit config.yaml with your file paths")
        print("2. Run: python main.py index   (to index your files)")
        print("3. Run: python main.py         (start interactive mode)")
        print()
        
        return True


if __name__ == '__main__':
    setup = JontySetup()
    success = setup.run()
    sys.exit(0 if success else 1)
