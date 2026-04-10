"""
Jonty AI Brain - LLM Interface
Handles inference, context building, and response generation
"""

import os
import json
from typing import Optional, Dict, List, Any
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Brain:
    """
    AI Brain module for Jonty
    Handles LLM interactions and reasoning
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Brain
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.model_path = config.get('model_path', '~/models/tinyllama.gguf')
        self.model_name = config.get('model_name', 'tinyllama')
        self.max_tokens = config.get('max_tokens', 512)
        self.temperature = config.get('temperature', 0.7)
        self.top_k = config.get('top_k', 40)
        self.top_p = config.get('top_p', 0.95)
        
        # Model state
        self.model = None
        self.is_loaded = False
        
        logger.info(f"Brain initialized: {self.model_name}")

    def load_model(self) -> bool:
        """
        Load the LLM model
        Supports: ollama, llama-cpp-python, or other backends
        
        Returns:
            bool: True if model loaded, False otherwise
        """
        try:
            # Try ollama first (recommended for TinyLlama)
            try:
                import ollama
                logger.info("Using Ollama backend...")
                self.model = ollama
                self.backend = "ollama"
                self.is_loaded = True
                return True
            except ImportError:
                logger.info("Ollama not found, trying llama-cpp-python...")
            
            # Fallback: llama-cpp-python
            try:
                from llama_cpp import Llama
                model_path = os.path.expanduser(self.model_path)
                
                if not os.path.exists(model_path):
                    logger.warning(f"Model not found at {model_path}")
                    logger.info("Please download TinyLlama from:")
                    logger.info("huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF")
                    return False
                
                logger.info(f"Loading model from {model_path}...")
                self.model = Llama(
                    model_path=model_path,
                    n_gpu_layers=-1 if self.config.get('use_gpu', False) else 0,
                    n_ctx=2048,
                    n_threads=4,
                    verbose=False
                )
                self.backend = "llama-cpp"
                self.is_loaded = True
                logger.info("Model loaded successfully!")
                return True
                
            except ImportError:
                logger.error("Neither Ollama nor llama-cpp-python installed!")
                logger.info("Install with: pip install ollama llama-cpp-python")
                return False
                
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False

    def generate_response(
        self,
        query: str,
        context: Optional[str] = None,
        tools_info: Optional[str] = None,
        memory: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Generate response from LLM
        
        Args:
            query: User's question
            context: Retrieved context from files
            tools_info: Available tools description
            memory: Previous conversation history
            
        Returns:
            dict: {response, reasoning, tool_call, confidence}
        """
        
        if not self.is_loaded:
            return {
                "response": "⚠️ Model not loaded. Please install model or backend.",
                "error": True,
                "tool_call": None
            }
        
        # Build prompt
        prompt = self._build_prompt(query, context, tools_info, memory)
        
        try:
            if self.backend == "ollama":
                return self._generate_ollama(prompt, query)
            else:
                return self._generate_llama_cpp(prompt, query)
                
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return {
                "response": f"Error generating response: {str(e)}",
                "error": True,
                "tool_call": None
            }

    def _build_prompt(
        self,
        query: str,
        context: Optional[str] = None,
        tools_info: Optional[str] = None,
        memory: Optional[List[Dict]] = None
    ) -> str:
        """Build structured prompt with context"""
        
        prompt = """You are Jonty, a personal AI assistant. Your role is to:
1. Answer questions based on provided context
2. Search user's files when needed
3. Use tools (calculator, alarms, file operations) when appropriate
4. Be helpful, accurate, and conversational

SYSTEM CAPABILITIES:
- Search local files (PDFs, documents, code, images)
- Perform calculations
- Set alarms and reminders
- Open/manage applications
- Extract information from documents

"""
        
        # Add tools info
        if tools_info:
            prompt += f"\nAVAILABLE TOOLS:\n{tools_info}\n"
        
        # Add conversation memory
        if memory:
            prompt += "CONVERSATION HISTORY:\n"
            for msg in memory[-5:]:  # Last 5 messages
                role = msg.get('role', 'user').upper()
                content = msg.get('content', '')
                prompt += f"{role}: {content}\n"
        
        # Add retrieved context
        if context:
            prompt += f"\nRELEVANT CONTEXT:\n{context}\n"
        
        # Add user query
        prompt += f"\nUSER QUERY:\n{query}\n"
        prompt += "\nRESPONSE:\n"
        
        return prompt

    def _generate_ollama(self, prompt: str, query: str) -> Dict[str, Any]:
        """Generate using Ollama backend"""
        try:
            response = self.model.generate(
                model='tinyllama',
                prompt=prompt,
                stream=False,
                options={
                    'temperature': self.temperature,
                    'top_k': self.top_k,
                    'top_p': self.top_p,
                }
            )
            
            text = response.get('response', '')
            return {
                "response": text.strip(),
                "query": query,
                "tool_call": self._extract_tool_call(text),
                "confidence": 0.85
            }
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return {
                "response": f"Error with Ollama: {str(e)}",
                "error": True
            }

    def _generate_llama_cpp(self, prompt: str, query: str) -> Dict[str, Any]:
        """Generate using llama-cpp-python backend"""
        try:
            response = self.model(
                prompt,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_k=self.top_k,
                top_p=self.top_p,
                stop=["USER:", "\n\n"]
            )
            
            text = response['choices'][0]['text']
            return {
                "response": text.strip(),
                "query": query,
                "tool_call": self._extract_tool_call(text),
                "confidence": 0.85
            }
        except Exception as e:
            logger.error(f"Llama-cpp error: {e}")
            return {
                "response": f"Error with llama-cpp: {str(e)}",
                "error": True
            }

    def _extract_tool_call(self, text: str) -> Optional[Dict]:
        """
        Extract tool calls from response
        Format: [TOOL: tool_name | ARGS: arg1=value1, arg2=value2]
        """
        import re
        
        pattern = r'\[TOOL:\s*(\w+)\s*\|\s*ARGS:\s*(.+?)\]'
        match = re.search(pattern, text)
        
        if match:
            tool_name = match.group(1)
            args_str = match.group(2)
            
            # Parse arguments
            args = {}
            for arg in args_str.split(','):
                key, val = arg.split('=')
                args[key.strip()] = val.strip()
            
            return {
                "tool": tool_name,
                "args": args
            }
        return None

    def is_question_about_files(self, query: str) -> bool:
        """Detect if query requires file search"""
        keywords = ['file', 'document', 'pdf', 'search', 'find', 'where', 'show me', 'look up']
        return any(kw in query.lower() for kw in keywords)

    def is_tool_request(self, query: str) -> bool:
        """Detect if query requires tool usage"""
        keywords = ['calculate', 'alarm', 'open', 'reminder', 'what time', 'weather', 'convert']
        return any(kw in query.lower() for kw in keywords)

    def summarize(self, text: str, max_length: int = 300) -> str:
        """Summarize long text"""
        if len(text) <= max_length:
            return text
        
        # Simple summarization: take first sentences until limit
        sentences = text.split('. ')
        summary = ''
        for sent in sentences:
            if len(summary) + len(sent) <= max_length:
                summary += sent + '. '
            else:
                break
        return summary.strip()
