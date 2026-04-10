"""
Vector Database - FAISS-based vector storage and retrieval
Stores embeddings and metadata for fast similarity search
"""

import logging
import json
import os
from typing import List, Dict, Tuple
import numpy as np

logger = logging.getLogger(__name__)


class VectorDB:
    """Manage FAISS vector database"""
    
    def __init__(self, index_path: str = "vector_db/faiss_index.bin", 
                 metadata_path: str = "vector_db/metadata.json",
                 embedding_dim: int = 384):
        """
        Args:
            index_path: Path to store FAISS index
            metadata_path: Path to store metadata
            embedding_dim: Dimension of embeddings
        """
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.embedding_dim = embedding_dim
        self.index = None
        self.metadata = []
        self.faiss = None
        self._load_faiss()
        self._load_or_create_index()
    
    def _load_faiss(self):
        """Load FAISS library"""
        try:
            import faiss
            self.faiss = faiss
            logger.info("FAISS loaded successfully")
        except ImportError:
            logger.error("FAISS not installed. Install with: pip install faiss-cpu")
            raise
    
    def _load_or_create_index(self):
        """Load existing index or create new one"""
        if os.path.exists(self.index_path):
            try:
                logger.info(f"Loading FAISS index from {self.index_path}")
                self.index = self.faiss.read_index(self.index_path)
                self._load_metadata()
                logger.info(f"Index loaded with {self.index.ntotal} vectors")
            except Exception as e:
                logger.warning(f"Failed to load index: {e}. Creating new index.")
                self._create_new_index()
        else:
            self._create_new_index()
    
    def _create_new_index(self):
        """Create a new FAISS index"""
        logger.info(f"Creating new FAISS index (dimension: {self.embedding_dim})")
        self.index = self.faiss.IndexFlatL2(self.embedding_dim)
        self.metadata = []
    
    def add_embeddings(self, embeddings: np.ndarray, metadata: List[Dict]) -> bool:
        """
        Add embeddings to index
        
        Args:
            embeddings: Array of shape (n, embedding_dim)
            metadata: List of metadata dicts (must have 'text' and 'source')
            
        Returns:
            Success status
        """
        try:
            if len(embeddings) != len(metadata):
                logger.error(f"Mismatch: {len(embeddings)} embeddings, {len(metadata)} metadata")
                return False
            
            if embeddings.shape[1] != self.embedding_dim:
                logger.error(f"Embedding dimension mismatch: {embeddings.shape[1]} vs {self.embedding_dim}")
                return False
            
            # Convert to float32 if needed
            embeddings = np.asarray(embeddings, dtype=np.float32)
            
            # Add to index
            self.index.add(embeddings)
            
            # Update metadata
            for i, meta in enumerate(metadata):
                meta['vector_id'] = len(self.metadata) + i
                self.metadata.append(meta)
            
            logger.info(f"Added {len(embeddings)} embeddings. Total: {self.index.ntotal}")
            return True
        
        except Exception as e:
            logger.error(f"Error adding embeddings: {str(e)}")
            return False
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Tuple[float, Dict]]:
        """
        Search for similar embeddings
        
        Args:
            query_embedding: Query embedding vector
            k: Number of results to return
            
        Returns:
            List of (distance, metadata) tuples
        """
        try:
            query_embedding = np.asarray([query_embedding], dtype=np.float32)
            distances, indices = self.index.search(query_embedding, k)
            
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.metadata):
                    results.append((distances[0][i], self.metadata[idx]))
            
            return results
        
        except Exception as e:
            logger.error(f"Error searching index: {str(e)}")
            return []
    
    def save(self) -> bool:
        """Save index and metadata to disk"""
        try:
            # Create directory if needed
            os.makedirs(os.path.dirname(self.index_path) or ".", exist_ok=True)
            os.makedirs(os.path.dirname(self.metadata_path) or ".", exist_ok=True)
            
            # Save index
            self.faiss.write_index(self.index, self.index_path)
            logger.info(f"Index saved to {self.index_path}")
            
            # Save metadata
            with open(self.metadata_path, 'w') as f:
                json.dump(self.metadata, f, indent=2)
            logger.info(f"Metadata saved to {self.metadata_path}")
            
            return True
        
        except Exception as e:
            logger.error(f"Error saving index: {str(e)}")
            return False
    
    def _load_metadata(self):
        """Load metadata from disk"""
        try:
            if os.path.exists(self.metadata_path):
                with open(self.metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                logger.info(f"Loaded {len(self.metadata)} metadata entries")
        except Exception as e:
            logger.warning(f"Failed to load metadata: {e}")
            self.metadata = []
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        return {
            'total_vectors': self.index.ntotal if self.index else 0,
            'embedding_dim': self.embedding_dim,
            'metadata_entries': len(self.metadata),
            'index_path': self.index_path,
            'metadata_path': self.metadata_path
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test VectorDB
    db = VectorDB(embedding_dim=384)
    
    # Create sample embeddings
    embeddings = np.random.randn(5, 384).astype(np.float32)
    metadata = [
        {'text': f'Sample text {i}', 'source': 'test.txt', 'chunk_id': i}
        for i in range(5)
    ]
    
    db.add_embeddings(embeddings, metadata)
    
    # Test search
    query = np.random.randn(384).astype(np.float32)
    results = db.search(query, k=3)
    
    print("Search results:")
    for distance, meta in results:
        print(f"  Distance: {distance:.4f}, Text: {meta['text']}")
    
    print(f"\nStats: {db.get_stats()}")
