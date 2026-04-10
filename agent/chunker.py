"""
Text Chunker - Split large documents into manageable chunks
Uses sliding window approach to preserve context
"""

import logging
from typing import List, Dict, Tuple
import re

logger = logging.getLogger(__name__)


class TextChunker:
    """Split text into chunks for embedding"""
    
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        """
        Args:
            chunk_size: Number of characters per chunk
            overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str, source: str = "unknown") -> List[Dict]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Text to chunk
            source: Source file/document identifier
            
        Returns:
            List of chunk dictionaries with text, metadata
        """
        chunks = []
        
        # Handle empty text
        if not text or len(text.strip()) == 0:
            logger.warning(f"Empty text from source: {source}")
            return chunks
        
        # Split by sentences to avoid breaking text awkwardly
        sentences = self._split_sentences(text)
        
        chunk_text = ""
        chunk_start = 0
        
        for i, sentence in enumerate(sentences):
            potential_chunk = chunk_text + sentence
            
            if len(potential_chunk) > self.chunk_size and chunk_text:
                # Save current chunk
                chunks.append({
                    'text': chunk_text.strip(),
                    'source': source,
                    'chunk_id': len(chunks),
                    'start_index': chunk_start,
                    'end_index': chunk_start + len(chunk_text)
                })
                
                # Start new chunk with overlap
                chunk_text = self._create_overlap(chunk_text) + sentence
                chunk_start = max(0, chunk_start + len(chunk_text) - self.overlap)
            else:
                chunk_text = potential_chunk
        
        # Add final chunk
        if chunk_text.strip():
            chunks.append({
                'text': chunk_text.strip(),
                'source': source,
                'chunk_id': len(chunks),
                'start_index': chunk_start,
                'end_index': chunk_start + len(chunk_text)
            })
        
        logger.info(f"Created {len(chunks)} chunks from {source}")
        return chunks
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitter (can be enhanced with NLTK)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s for s in sentences if s.strip()]
    
    def _create_overlap(self, text: str) -> str:
        """Get last N characters for overlap"""
        if len(text) <= self.overlap:
            return text
        return text[-self.overlap:]
    
    def chunk_documents(self, documents: Dict[str, str]) -> List[Dict]:
        """
        Chunk multiple documents
        
        Args:
            documents: Dict of {source: text}
            
        Returns:
            Combined list of chunks
        """
        all_chunks = []
        for source, text in documents.items():
            chunks = self.chunk_text(text, source)
            all_chunks.extend(chunks)
        return all_chunks


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    chunker = TextChunker(chunk_size=256, overlap=50)
    
    sample_text = """
    This is a sample document. It contains multiple sentences.
    Each sentence will be grouped into chunks. The chunks will have overlaps.
    This helps preserve context when processing documents.
    Machine learning models work better with properly chunked text.
    """
    
    chunks = chunker.chunk_text(sample_text, "sample.txt")
    for chunk in chunks:
        print(f"Chunk {chunk['chunk_id']}:")
        print(f"  Text: {chunk['text'][:100]}...")
        print()
