"""
Indexer - Main orchestrator for creating and maintaining the vector index
Scans files → Load → Chunk → Embed → Store
"""

import logging
import os
from pathlib import Path
from typing import List, Dict
import yaml

from agent.loader import FileLoader
from agent.chunker import TextChunker
from agent.embedder import Embedder
from agent.vector_db import VectorDB

logger = logging.getLogger(__name__)


class Indexer:
    """Main indexer that orchestrates the entire pipeline"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.loader = FileLoader()
        self.chunker = TextChunker(
            chunk_size=self.config['vector_db']['chunk_size'],
            overlap=self.config['vector_db']['overlap']
        )
        self.embedder = Embedder(
            model_name=self.config['embedding']['model_name'],
            device=self.config['embedding']['device']
        )
        self.vector_db = VectorDB(
            index_path=self.config['vector_db']['index_path'],
            metadata_path=self.config['vector_db']['metadata_path'],
            embedding_dim=self.config['embedding']['embedding_dim']
        )
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            raise
    
    def index_paths(self) -> Dict[str, int]:
        """
        Index all configured paths
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            'total_files': 0,
            'indexed_files': 0,
            'total_chunks': 0,
            'total_embeddings': 0,
            'failed_files': []
        }
        
        paths = self.config.get('paths', [])
        
        for path_str in paths:
            path = Path(path_str).expanduser()
            if path.exists() and path.is_dir():
                logger.info(f"Indexing path: {path}")
                file_stats = self._index_directory(str(path))
                
                # Accumulate stats
                stats['total_files'] += file_stats['total_files']
                stats['indexed_files'] += file_stats['indexed_files']
                stats['total_chunks'] += file_stats['total_chunks']
                stats['total_embeddings'] += file_stats['total_embeddings']
                stats['failed_files'].extend(file_stats['failed_files'])
        
        # Save the vector database
        logger.info("Saving vector database...")
        self.vector_db.save()
        
        return stats
    
    def _index_directory(self, directory_path: str) -> Dict:
        """Index files in a directory"""
        stats = {
            'total_files': 0,
            'indexed_files': 0,
            'total_chunks': 0,
            'total_embeddings': 0,
            'failed_files': []
        }
        
        documents = self.loader.load_directory(directory_path, recursive=True)
        
        if not documents:
            logger.warning(f"No supported files found in {directory_path}")
            return stats
        
        stats['total_files'] = len(documents)
        
        try:
            # Chunk all documents
            logger.info(f"Chunking {len(documents)} documents...")
            chunks = self.chunker.chunk_documents(documents)
            stats['total_chunks'] = len(chunks)
            
            if not chunks:
                logger.warning("No chunks created")
                return stats
            
            # Embed chunks
            logger.info(f"Embedding {len(chunks)} chunks...")
            embeddings, chunks = self.embedder.embed_chunks(chunks)
            stats['total_embeddings'] = len(embeddings)
            
            # Add to vector database
            logger.info("Adding embeddings to vector database...")
            success = self.vector_db.add_embeddings(embeddings, chunks)
            
            if success:
                stats['indexed_files'] = len(documents)
                logger.info(f"Successfully indexed {len(documents)} files")
            else:
                stats['failed_files'] = list(documents.keys())
        
        except Exception as e:
            logger.error(f"Error indexing directory: {e}")
            stats['failed_files'] = list(documents.keys())
        
        return stats
    
    def get_stats(self) -> Dict:
        """Get current database statistics"""
        return self.vector_db.get_stats()
    
    def index_single_file(self, file_path: str) -> bool:
        """Index a single file"""
        try:
            logger.info(f"Indexing file: {file_path}")
            
            # Load file
            content = self.loader.load_file(file_path)
            if not content:
                logger.error(f"Failed to load file: {file_path}")
                return False
            
            # Chunk
            chunks = self.chunker.chunk_text(content, file_path)
            if not chunks:
                logger.error(f"No chunks created from: {file_path}")
                return False
            
            # Embed
            embeddings, chunks = self.embedder.embed_chunks(chunks)
            
            # Add to DB
            success = self.vector_db.add_embeddings(embeddings, chunks)
            
            if success:
                self.vector_db.save()
                logger.info(f"Successfully indexed: {file_path}")
            
            return success
        
        except Exception as e:
            logger.error(f"Error indexing file: {e}")
            return False


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create indexer and run
    try:
        indexer = Indexer()
        logger.info("Starting indexing...")
        stats = indexer.index_paths()
        
        print("\n" + "="*50)
        print("INDEXING COMPLETE")
        print("="*50)
        print(f"Total files scanned: {stats['total_files']}")
        print(f"Files indexed: {stats['indexed_files']}")
        print(f"Total chunks created: {stats['total_chunks']}")
        print(f"Total embeddings: {stats['total_embeddings']}")
        if stats['failed_files']:
            print(f"Failed files: {len(stats['failed_files'])}")
        
        print("\nVector DB Stats:")
        db_stats = indexer.get_stats()
        for key, value in db_stats.items():
            print(f"  {key}: {value}")
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
