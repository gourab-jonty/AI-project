@echo off
REM Jonty - Automated Setup Script for Windows
REM Usage: python setup.py

echo.
echo ======================================
echo   Jonty Setup Automation (Windows)
echo ======================================
echo.

REM Check Python version
echo [*] Checking Python version...
python --version
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

REM Create virtual environment
echo [*] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo [OK] venv created
) else (
    echo [OK] venv already exists
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo [*] Installing dependencies...
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed

REM Create directories
echo [*] Creating necessary directories...
if not exist "models" mkdir models
if not exist "logs" mkdir logs
if not exist "vector_db" mkdir vector_db
echo [OK] Directories created

REM Download model (optional)
echo.
set /p download_model="Download TinyLlama model? (y/n): "
if /i "%download_model%"=="y" (
    echo [*] Downloading TinyLlama model (~1.1GB)...
    cd models
    if not exist "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf" (
        echo [*] This may take 2-5 minutes...
        powershell -Command "(New-Object System.Net.ServicePointManager).SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf' -OutFile 'tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf'"
        echo [OK] Model downloaded
    ) else (
        echo [OK] Model already exists
    )
    cd ..
)

echo.
echo ======================================
echo   [OK] Setup Complete!
echo ======================================
echo.
echo Next steps:
echo 1. Edit config.yaml with your file paths
echo 2. Run: python main.py index   (to index your files)
echo 3. Run: python main.py         (start interactive mode)
echo.
pause
