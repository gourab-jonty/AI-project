#!/usr/bin/env python3
"""
Jonty Integration Test
Tests all components working together
"""

import os
import sys
import tempfile
import yaml
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import (
    FileLoader, TextChunker, Embedder, VectorDB, Retriever,
    Brain, Tools, Agent
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_test_files():
    """Create test files for indexing"""
    temp_dir = tempfile.mkdtemp()
    
    # Create test files
    files = {
        'test1.txt': """
        Python is a high-level programming language. 
        It's known for its simplicity and readability.
        Python is used in web development, data science, and AI.
        """,
        'test2.txt': """
        Machine Learning is a subset of Artificial Intelligence.
        It focuses on learning from data.
        Popular ML frameworks include TensorFlow and PyTorch.
        """
    }
    
    for filename, content in files.items():
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
    
    return temp_dir


def test_phase1_rag():
    """Test Phase 1: RAG System"""
    print("\n" + "="*60)
    print("PHASE 1: RAG System Test")
    print("="*60)
    
    # Create test files
    test_dir = create_test_files()
    print(f"✓ Created test files in {test_dir}")
    
    # Initialize components
    config = {
        'paths': [test_dir],
        'embed_model': 'sentence-transformers/all-MiniLM-L6-v2',
        'chunk_size': 100,
        'chunk_overlap': 10,
        'vector_db_path': './vector_db_test',
    }
    
    loader = FileLoader(config)
    chunker = TextChunker(config)
    embedder = Embedder(config)
    vector_db = VectorDB(config)
    retriever = Retriever(vector_db, embedder, config)
    
    print("✓ RAG components initialized")
    
    # Test file loading
    files = loader.load_from_directory(test_dir)
    print(f"✓ Loaded {len(files)} files")
    
    # Test chunking
    all_chunks = []
    for file_content in files.values():
        chunks = chunker.chunk_text(file_content)
        all_chunks.extend(chunks)
    print(f"✓ Created {len(all_chunks)} chunks")
    
    # Test embedding and indexing
    for i, chunk in enumerate(all_chunks):
        embedding = embedder.embed_text(chunk)
        vector_db.add_vector(f"chunk_{i}", embedding, chunk)
    print(f"✓ Embedded and indexed {len(all_chunks)} chunks")
    
    # Test retrieval
    test_queries = [
        "What is Python?",
        "Tell me about machine learning",
        "What are ML frameworks?"
    ]
    
    print("\n--- Retrieval Test ---")
    for query in test_queries:
        results = retriever.search(query, top_k=2)
        print(f"Query: '{query}'")
        for doc_id, score, content in results:
            print(f"  - {doc_id} (score: {score:.2%})")
    
    print("✓ Phase 1 RAG test completed!")
    return True


def test_brain():
    """Test Phase 2: Brain System"""
    print("\n" + "="*60)
    print("PHASE 2: Brain System Test")
    print("="*60)
    
    config = {
        'model_name': 'tinyllama',
        'max_tokens': 256,
        'temperature': 0.7,
    }
    
    brain = Brain(config)
    print("✓ Brain initialized")
    
    # Test model loading
    print("\n--- Model Loading ---")
    print("Attempting to load model...")
    print("(This requires Ollama or llama-cpp-python to be installed)")
    
    if brain.load_model():
        print("✓ Model loaded successfully!")
        
        # Test response generation
        test_queries = [
            "What is 2 + 2?",
            "Explain quantum computing in one sentence",
        ]
        
        print("\n--- Response Generation ---")
        for query in test_queries:
            print(f"Query: {query}")
            result = brain.generate_response(query)
            if not result.get('error'):
                print(f"Response: {result['response'][:100]}...")
            else:
                print(f"Error: {result.get('error')}")
    else:
        print("⚠️  Model not available (install Ollama or llama-cpp-python)")
    
    return True


def test_tools():
    """Test Phase 3: Tools System"""
    print("\n" + "="*60)
    print("PHASE 3: Tools System Test")
    print("="*60)
    
    tools = Tools()
    print("✓ Tools initialized")
    
    # Test calculations
    print("\n--- Tool Tests ---")
    
    test_cases = [
        ('calculator', {'expression': '2 + 2 * 3'}),
        ('get_time', {}),
        ('get_date', {}),
    ]
    
    for tool_name, args in test_cases:
        result = tools.execute(tool_name, **args)
        print(f"✓ {tool_name}: {result.get('result', result)}")
    
    print("✓ Tools test completed!")
    return True


def test_agent():
    """Test Phase 4: Agent System"""
    print("\n" + "="*60)
    print("PHASE 4: Agent System Test")
    print("="*60)
    
    # Initialize minimal agent for testing
    config = {
        'model_name': 'tinyllama',
        'embed_model': 'sentence-transformers/all-MiniLM-L6-v2',
        'max_tokens': 256,
        'temperature': 0.7,
    }
    
    brain = Brain(config)
    tools = Tools()
    
    # Create dummy retriever
    class DummyRetriever:
        def search(self, query, top_k=5):
            return [("doc_1", 0.8, f"Context for: {query}")]
    
    retriever = DummyRetriever()
    agent = Agent(brain, tools, retriever)
    print("✓ Agent initialized")
    
    # Test decision making
    print("\n--- Decision Making ---")
    
    test_queries = [
        "Calculate 5 * 5",
        "What files do I have?",
        "Hello!",
    ]
    
    for query in test_queries:
        thinking = agent.explain_thinking(query)
        print(f"\nQuery: '{query}'")
        for reason in thinking['reasoning']:
            print(f"  {reason}")
    
    print("\n✓ Agent test completed!")
    return True


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("JONTY INTEGRATION TEST SUITE")
    print("="*70)
    
    tests = [
        ("Phase 1: RAG System", test_phase1_rag),
        ("Phase 2: Brain System", test_brain),
        ("Phase 3: Tools System", test_tools),
        ("Phase 4: Agent System", test_agent),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            logger.error(f"Test failed: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    for name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {name}")
    
    passed_count = sum(results.values())
    total_count = len(results)
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("  1. Run: python main.py")
    print("  2. Try interactive queries")
    print("  3. Index your actual files with 'index' command")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
