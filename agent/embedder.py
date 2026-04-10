"""
Embedder - Convert text chunks to vector embeddings
Uses sentence-transformers for efficient CPU-based embeddings
"""

import logging
from typing import List, Dict, Tuple
import numpy as np

logger = logging.getLogger(__name__)


class Embedder:
    """Convert text to embeddings"""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", device: str = "cpu"):
        """
        Args:
            model_name: HuggingFace model identifier
            device: "cpu" or "cuda"
        """
        self.model_name = model_name
        self.device = device
        self.model = None
        self.embedding_dim = None
        self._load_model()
    
    def _load_model(self):
        """Load the embedding model"""
        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name, device=self.device)
            self.embedding_dim = self.model.get_sentence_embedding_dimension()
            logger.info(f"Model loaded. Embedding dimension: {self.embedding_dim}")
        except ImportError:
            logger.error("sentence-transformers not installed. Install with: pip install sentence-transformers")
            raise
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Convert single text to embedding
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        if not text or len(text.strip()) == 0:
            logger.warning("Empty text provided to embed")
            return np.zeros(self.embedding_dim)
        
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding
        except Exception as e:
            logger.error(f"Error embedding text: {str(e)}")
            return np.zeros(self.embedding_dim)
    
    def embed_batch(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Convert multiple texts to embeddings
        
        Args:
            texts: List of texts to embed
            batch_size: Batch size for processing
            
        Returns:
            Array of embeddings (n_texts, embedding_dim)
        """
        if not texts:
            logger.warning("No texts provided to embed")
            return np.array([])
        
        try:
            logger.info(f"Embedding {len(texts)} texts...")
            embeddings = self.model.encode(texts, batch_size=batch_size, convert_to_numpy=True)
            logger.info(f"Embedding complete. Shape: {embeddings.shape}")
            return embeddings
        except Exception as e:
            logger.error(f"Error embedding batch: {str(e)}")
            return np.array([])
    
    def embed_chunks(self, chunks: List[Dict]) -> Tuple[np.ndarray, List[Dict]]:
        """
        Embed a list of chunks
        
        Args:
            chunks: List of chunk dictionaries with 'text' field
            
        Returns:
            Tuple of (embeddings array, chunks list)
        """
        texts = [chunk['text'] for chunk in chunks]
        embeddings = self.embed_batch(texts)
        return embeddings, chunks


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    embedder = Embedder()
    
    # Test embedding
    sample_texts = [
        "The cat sat on the mat",
        "Machine learning is powerful",
        "Python is a great language"
    ]
    
    embeddings = embedder.embed_batch(sample_texts)
    print(f"Embeddings shape: {embeddings.shape}")
    print(f"First embedding: {embeddings[0][:5]}...")
