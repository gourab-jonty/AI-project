"""
File Loader - Extract text from various file formats
Supports: PDF, TXT, DOCX, MD, PY, JSON, CSV, XLSX, etc.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
import logging

# Setup logging
logger = logging.getLogger(__name__)

class FileLoader:
    """Load and extract text from different file formats"""
    
    SUPPORTED_FORMATS = {
        '.pdf': 'pdf',
        '.txt': 'text',
        '.md': 'text',
        '.py': 'text',
        '.js': 'text',
        '.ts': 'text',
        '.java': 'text',
        '.cpp': 'text',
        '.c': 'text',
        '.h': 'text',
        '.json': 'text',
        '.yaml': 'text',
        '.yml': 'text',
        '.xml': 'text',
        '.csv': 'csv',
        '.xlsx': 'excel',
        '.xls': 'excel',
        '.docx': 'docx',
        '.doc': 'docx',
    }
    
    def __init__(self):
        self.supported_types = set(self.SUPPORTED_FORMATS.keys())
    
    def load_file(self, file_path: str) -> Optional[str]:
        """Load a single file and return its content"""
        try:
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext not in self.supported_types:
                logger.warning(f"Unsupported file type: {file_ext}")
                return None
            
            file_type = self.SUPPORTED_FORMATS[file_ext]
            
            if file_type == 'text':
                return self._load_text(file_path)
            elif file_type == 'pdf':
                return self._load_pdf(file_path)
            elif file_type == 'docx':
                return self._load_docx(file_path)
            elif file_type == 'csv':
                return self._load_csv(file_path)
            elif file_type == 'excel':
                return self._load_excel(file_path)
            
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {str(e)}")
            return None
    
    def _load_text(self, file_path: str) -> str:
        """Load plain text files"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    def _load_pdf(self, file_path: str) -> str:
        """Load PDF files using PyMuPDF"""
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(file_path)
            text = ""
            for page_num in range(len(doc)):
                page = doc[page_num]
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page.get_text()
            doc.close()
            return text
        except ImportError:
            logger.warning("PyMuPDF not installed. Install with: pip install PyMuPDF")
            return ""
    
    def _load_docx(self, file_path: str) -> str:
        """Load DOCX files"""
        try:
            from docx import Document
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except ImportError:
            logger.warning("python-docx not installed. Install with: pip install python-docx")
            return ""
    
    def _load_csv(self, file_path: str) -> str:
        """Load CSV files"""
        try:
            import pandas as pd
            df = pd.read_csv(file_path)
            return df.to_string()
        except ImportError:
            logger.warning("Pandas not installed. Install with: pip install pandas")
            return ""
    
    def _load_excel(self, file_path: str) -> str:
        """Load Excel files"""
        try:
            import pandas as pd
            excel_file = pd.ExcelFile(file_path)
            text = ""
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                text += f"\n--- Sheet: {sheet_name} ---\n"
                text += df.to_string()
            return text
        except ImportError:
            logger.warning("Pandas not installed. Install with: pip install pandas openpyxl")
            return ""
    
    def load_directory(self, directory_path: str, recursive: bool = True) -> Dict[str, str]:
        """Load all supported files from a directory"""
        documents = {}
        path = Path(directory_path).expanduser()
        
        if not path.exists():
            logger.error(f"Directory not found: {directory_path}")
            return documents
        
        pattern = "**/*" if recursive else "*"
        
        for file_path in path.glob(pattern):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_types:
                logger.info(f"Loading: {file_path}")
                content = self.load_file(str(file_path))
                if content:
                    documents[str(file_path)] = content
        
        return documents


if __name__ == "__main__":
    # Test the loader
    logging.basicConfig(level=logging.INFO)
    loader = FileLoader()
    
    # Test with a sample file
    test_file = "config.yaml"
    if os.path.exists(test_file):
        content = loader.load_file(test_file)
        print(f"Loaded {test_file}:")
        print(content[:200] + "...")
