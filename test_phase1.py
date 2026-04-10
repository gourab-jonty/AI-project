#!/usr/bin/env python3
"""
Test script for Jonty - Personal AI Assistant
Demonstrates the RAG pipeline
"""

import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from indexer import Indexer
from agent.retriever import Retriever

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_phase1():
    """Test Phase 1: Data Engine"""
    print("\n" + "="*60)
    print("PHASE 1: DATA ENGINE TEST")
    print("="*60)
    
    try:
        # Initialize indexer
        print("\n1. Initializing indexer...")
        indexer = Indexer()
        print("   ✓ Indexer initialized")
        
        # Index paths
        print("\n2. Indexing configured paths...")
        stats = indexer.index_paths()
        
        print("\n   Indexing Results:")
        print(f"   - Total files scanned: {stats['total_files']}")
        print(f"   - Files indexed: {stats['indexed_files']}")
        print(f"   - Total chunks: {stats['total_chunks']}")
        print(f"   - Total embeddings: {stats['total_embeddings']}")
        
        if stats['failed_files']:
            print(f"   - Failed files: {len(stats['failed_files'])}")
        
        print("\n   ✓ Indexing complete")
        
        # Test retrieval
        if stats['total_embeddings'] > 0:
            print("\n3. Testing retrieval...")
            retriever = Retriever(
                embedder=indexer.embedder,
                vector_db=indexer.vector_db,
                top_k=5
            )
            
            # Test query
            test_queries = [
                "configuration",
                "python",
                "setup"
            ]
            
            for query in test_queries:
                print(f"\n   Query: '{query}'")
                results = retriever.search(query, k=3)
                
                if results:
                    for i, result in enumerate(results, 1):
                        print(f"   Result {i}:")
                        print(f"     Source: {result.get('source', 'unknown')}")
                        print(f"     Similarity: {result.get('similarity', 0):.2%}")
                        text_preview = result.get('text', '')[:100]
                        print(f"     Text: {text_preview}...")
                else:
                    print("   No results found")
            
            print("\n   ✓ Retrieval test complete")
        else:
            print("\n   ⚠ No embeddings to test retrieval")
        
        print("\n" + "="*60)
        print("PHASE 1 TEST COMPLETE ✓")
        print("="*60)
        
        return True
    
    except Exception as e:
        logger.error(f"Test failed: {e}")
        print("\n" + "="*60)
        print("PHASE 1 TEST FAILED ✗")
        print("="*60)
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("JONTY - PERSONAL AI ASSISTANT")
    print("Phase 1: Data Engine Test")
    print("="*60)
    
    success = test_phase1()
    
    if success:
        print("\n✓ All tests passed!")
        print("\nNext Steps:")
        print("1. Phase 2: Build LLM Brain (model loading)")
        print("2. Phase 3: Build Tools System (calculator, etc)")
        print("3. Phase 4: Build Agent Router (decision making)")
        print("4. Phase 5: Build UI")
        sys.exit(0)
    else:
        print("\n✗ Tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
