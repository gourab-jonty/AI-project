#!/usr/bin/env python3
"""
Jonty - Personal AI Assistant
Main entry point and interface
"""

import os
import sys
import yaml
import logging
import json
from pathlib import Path
from typing import Optional

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import (
    FileLoader, TextChunker, Embedder, VectorDB, Retriever,
    Brain, Tools, Agent
)
from indexer import Indexer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/jonty.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class Jonty:
    """Main Jonty Application"""
    
    def __init__(self, config_path: str = 'config.yaml'):
        """
        Initialize Jonty
        
        Args:
            config_path: Path to configuration file
        """
        logger.info("🚀 Starting Jonty AI Assistant...")
        
        # Load config
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.indexer = Indexer(self.config)
        
        # Initialize RAG components
        logger.info("Initializing RAG components...")
        self.loader = FileLoader(self.config)
        self.chunker = TextChunker(self.config)
        self.embedder = Embedder(self.config)
        self.vector_db = VectorDB(self.config)
        self.retriever = Retriever(self.vector_db, self.embedder, self.config)
        
        # Initialize Brain and Tools
        logger.info("Initializing Brain and Tools...")
        self.brain = Brain(self.config)
        self.tools = Tools()
        
        # Initialize Agent
        self.agent = Agent(self.brain, self.tools, self.retriever)
        
        logger.info("✅ Jonty initialized successfully!")
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Config loaded from {config_path}")
            return config
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}")
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """Get default configuration"""
        return {
            'paths': [os.path.expanduser('~'), './'],
            'model_name': 'tinyllama',
            'embed_model': 'sentence-transformers/all-MiniLM-L6-v2',
            'chunk_size': 500,
            'chunk_overlap': 50,
            'vector_db_path': './vector_db',
            'max_tokens': 512,
            'temperature': 0.7,
        }
    
    def index_files(self, paths: Optional[list] = None) -> dict:
        """
        Index local files
        
        Args:
            paths: Paths to index (default from config)
            
        Returns:
            Indexing status
        """
        paths = paths or self.config.get('paths', [])
        logger.info(f"Starting indexing of {len(paths)} path(s)...")
        
        result = self.indexer.index_files()
        logger.info(f"Indexed {result['total_files']} files, {result['total_chunks']} chunks")
        
        return result
    
    def query(self, query: str, search_files: bool = True) -> dict:
        """
        Process a user query
        
        Args:
            query: User's question or command
            search_files: Whether to search local files
            
        Returns:
            Response with answer and metadata
        """
        logger.info(f"Processing query: {query}")
        
        # Check if brain is loaded
        if not self.brain.is_loaded:
            logger.warning("Brain not loaded. Loading model...")
            if not self.brain.load_model():
                return {
                    'success': False,
                    'error': '❌ Failed to load language model. Please install Ollama or llama-cpp-python',
                    'info': 'Download from: https://ollama.ai or pip install llama-cpp-python'
                }
        
        # Process query through agent
        response = self.agent.process_query(query, search_files=search_files)
        
        return response
    
    def chat_repl(self):
        """Interactive chat mode"""
        print("\n" + "="*60)
        print("🤖 Jonty - Personal AI Assistant")
        print("="*60)
        print("Type 'help' for commands, 'quit' to exit\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'quit':
                    print("Goodbye! 👋")
                    break
                
                if user_input.lower() == 'help':
                    self._print_help()
                    continue
                
                if user_input.lower() == 'memory':
                    self._print_memory()
                    continue
                
                if user_input.lower().startswith('index'):
                    result = self.index_files()
                    print(f"\n📊 {result}")
                    continue
                
                # Process query
                result = self.query(user_input)
                
                if result.get('success'):
                    print(f"\nJonty: {result['response']}")
                    
                    if result.get('tool_used'):
                        print(f"  🧰 Tool used: {result.get('tool_result', {}).get('tool')}")
                    
                    if result.get('context_used'):
                        print(f"  📄 (Used file context)")
                else:
                    print(f"\n❌ Error: {result.get('error')}")
                
                print()
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except Exception as e:
                logger.error(f"Chat error: {e}")
                print(f"Error: {str(e)}")
    
    def _print_help(self):
        """Print help information"""
        help_text = """
JONTY COMMANDS:
  help          - Show this help message
  quit          - Exit Jonty
  memory        - Show conversation history
  index         - Re-index local files
  
QUERY EXAMPLES:
  "What's the weather?"           - Ask questions
  "Open my documents"             - Use tools
  "Search for PDFs about Python"  - Search files
  "Calculate 2 + 2"               - Calculations
  "Set an alarm for 3 PM"         - Schedule tasks
        """
        print(help_text)
    
    def _print_memory(self):
        """Print conversation memory"""
        memory = self.agent.get_memory()
        if not memory:
            print("No conversation history yet.")
            return
        
        print("\n" + "="*60)
        print("CONVERSATION HISTORY")
        print("="*60)
        for msg in memory:
            role = msg['role'].upper()
            content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
            print(f"{role}: {content}")
        print("="*60 + "\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Jonty - Personal AI Assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Interactive mode
  python main.py "What files do I have?"  # Single query
  python main.py index              # Index files
        """
    )
    
    parser.add_argument(
        'query',
        nargs='?',
        help='Query to process (leave empty for interactive mode)'
    )
    
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to config file'
    )
    
    parser.add_argument(
        '--no-files',
        action='store_true',
        help='Do not search files'
    )
    
    args = parser.parse_args()
    
    # Initialize Jonty
    jonty = Jonty(args.config)
    
    # Handle different modes
    if args.query is None:
        # Interactive mode
        jonty.chat_repl()
    elif args.query.lower() == 'index':
        # Index mode
        result = jonty.index_files()
        print(json.dumps(result, indent=2))
    else:
        # Single query mode
        result = jonty.query(args.query, search_files=not args.no_files)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
