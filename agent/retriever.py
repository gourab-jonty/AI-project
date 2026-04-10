"""
Retriever - Search the vector database for relevant information
Uses RAG (Retrieval-Augmented Generation) to find context
"""

import logging
from typing import List, Dict, Tuple
import numpy as np

from agent.embedder import Embedder
from agent.vector_db import VectorDB

logger = logging.getLogger(__name__)


class Retriever:
    """Retrieve relevant documents from vector database"""
    
    def __init__(self, embedder: Embedder, vector_db: VectorDB, top_k: int = 5, 
                 similarity_threshold: float = 0.5):
        """
        Args:
            embedder: Embedder instance
            vector_db: VectorDB instance
            top_k: Number of results to return
            similarity_threshold: Minimum similarity score (0-1)
        """
        self.embedder = embedder
        self.vector_db = vector_db
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold
    
    def search(self, query: str, k: int = None) -> List[Dict]:
        """
        Search for relevant documents
        
        Args:
            query: Search query
            k: Number of results (uses self.top_k if not specified)
            
        Returns:
            List of relevant document chunks with metadata
        """
        if k is None:
            k = self.top_k
        
        try:
            logger.info(f"Searching for: '{query}'")
            
            # Embed query
            query_embedding = self.embedder.embed_text(query)
            
            # Search
            results = self.vector_db.search(query_embedding, k=k * 2)  # Get more, then filter
            
            # Convert distances to cosine similarity (L2 distance → similarity)
            # Lower L2 distance = higher similarity
            filtered_results = []
            for distance, metadata in results:
                # Convert L2 distance to similarity score (0-1)
                # Using formula: similarity = 1 / (1 + distance)
                similarity = 1.0 / (1.0 + distance)
                
                if similarity >= self.similarity_threshold:
                    result = dict(metadata)
                    result['similarity'] = similarity
                    result['distance'] = distance
                    filtered_results.append(result)
            
            # Return top k
            filtered_results = sorted(filtered_results, key=lambda x: x['similarity'], reverse=True)[:k]
            
            logger.info(f"Found {len(filtered_results)} relevant results")
            return filtered_results
        
        except Exception as e:
            logger.error(f"Error searching: {e}")
            return []
    
    def search_by_keywords(self, keywords: List[str], k: int = None) -> List[Dict]:
        """
        Search using multiple keywords (OR logic)
        
        Args:
            keywords: List of keywords
            k: Number of results
            
        Returns:
            Combined search results
        """
        all_results = {}
        
        for keyword in keywords:
            results = self.search(keyword, k=k or self.top_k)
            for result in results:
                result_id = (result['source'], result['chunk_id'])
                if result_id not in all_results:
                    all_results[result_id] = result
        
        # Sort by similarity
        sorted_results = sorted(all_results.values(), 
                               key=lambda x: x['similarity'], 
                               reverse=True)
        return sorted_results[:k or self.top_k]
    
    def get_context(self, query: str, num_chunks: int = None) -> str:
        """
        Get formatted context for LLM
        
        Args:
            query: Search query
            num_chunks: Number of context chunks
            
        Returns:
            Formatted context string
        """
        if num_chunks is None:
            num_chunks = self.top_k
        
        results = self.search(query, k=num_chunks)
        
        if not results:
            return "No relevant information found."
        
        context = "RELEVANT CONTEXT:\n"
        context += "=" * 50 + "\n\n"
        
        for i, result in enumerate(results, 1):
            context += f"[Source {i}: {result.get('source', 'unknown')}]\n"
            context += f"Relevance: {result.get('similarity', 0):.2%}\n"
            context += f"Text: {result.get('text', '')[:300]}...\n"
            context += "-" * 50 + "\n\n"
        
        return context
    
    def update_thresholds(self, top_k: int = None, similarity_threshold: float = None):
        """Update retrieval parameters"""
        if top_k is not None:
            self.top_k = top_k
            logger.info(f"Top-k updated to {top_k}")
        
        if similarity_threshold is not None:
            self.similarity_threshold = similarity_threshold
            logger.info(f"Similarity threshold updated to {similarity_threshold}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Note: This is a demo. In real usage, embedder and vector_db 
    # would be initialized from actual data
    
    print("Retriever module loaded successfully")
    print("Use with Embedder and VectorDB instances")
