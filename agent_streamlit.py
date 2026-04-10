"""
Jonty Web UI - Streamlit Interface
Beautiful web dashboard for Jonty AI Assistant
"""

import streamlit as st
import os
import sys
import yaml
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import Brain, Tools, Agent
from agent.retriever import Retriever
from agent.embedder import Embedder
from agent.vector_db import VectorDB
from indexer import Indexer

# Page config
st.set_page_config(
    page_title="🤖 Jonty - AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5em;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1em;
    }
    .stChat {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_jonty():
    """Load Jonty components (cached)"""
    config_path = 'config.yaml'
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    embedder = Embedder(config)
    vector_db = VectorDB(config)
    retriever = Retriever(vector_db, embedder, config)
    brain = Brain(config)
    tools = Tools()
    agent = Agent(brain, tools, retriever)
    
    return agent, config

def main():
    """Main Streamlit app"""
    
    st.markdown('<h1 class="main-header">🤖 Jonty - Personal AI Assistant</h1>', unsafe_allow_html=True)
    
    # Load components
    agent, config = load_jonty()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Mode selection
        mode = st.radio(
            "Select Mode",
            ["💬 Chat", "🔍 Search Files", "🧰 Tools", "📊 Memory", "⚙️ Config"]
        )
        
        # Search settings
        if mode == "🔍 Search Files":
            search_depth = st.slider("Search Depth", 1, 10, 5)
        
        # Model settings
        st.subheader("Model Settings")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
        max_tokens = st.slider("Max Tokens", 100, 2000, 512)
        
        # File management
        st.subheader("File Management")
        if st.button("📁 Index Files"):
            with st.spinner("Indexing files..."):
                indexer = Indexer(config)
                result = indexer.index_files()
                st.success(f"✅ Indexed {result['total_files']} files, {result['total_chunks']} chunks")
        
        if st.button("🗑️ Clear Memory"):
            agent.clear_memory()
            st.success("Memory cleared!")
    
    # Main content
    if mode == "💬 Chat":
        st.subheader("Chat with Jonty")
        
        # Display conversation history
        if agent.memory:
            with st.expander("📜 Conversation History"):
                for msg in agent.memory:
                    role = "👤 You" if msg['role'] == 'user' else "🤖 Jonty"
                    st.write(f"**{role}:** {msg['content']}")
        
        # Chat input
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input(
                "Ask Jonty anything:",
                placeholder="What Python files do I have? Calculate 2+2? etc."
            )
        with col2:
            search_files = st.checkbox("Search files", value=True)
        
        if user_input:
            with st.spinner("🤔 Thinking..."):
                response = agent.process_query(user_input, search_files=search_files)
            
            # Display response
            st.markdown(f"**🤖 Jonty:** {response['response']}")
            
            # Show metadata
            col1, col2, col3 = st.columns(3)
            with col1:
                if response.get('context_used'):
                    st.info("📄 Used file context")
            with col2:
                if response.get('tool_used'):
                    st.info(f"🧰 Tool: {response.get('tool_result', {}).get('tool', '?')}")
            with col3:
                st.metric("Confidence", f"{response.get('confidence', 0.7):.0%}")
    
    elif mode == "🔍 Search Files":
        st.subheader("Search Your Files")
        
        search_query = st.text_input("Search for:", placeholder="Python files, PDFs about ML, etc.")
        
        if search_query:
            with st.spinner("Searching..."):
                results = agent.retriever.search(search_query, top_k=5)
            
            if results:
                st.success(f"Found {len(results)} results")
                for i, (doc_id, score, content) in enumerate(results, 1):
                    with st.expander(f"📄 Result {i} (relevance: {score:.0%})"):
                        st.write(content[:500] + "..." if len(content) > 500 else content)
            else:
                st.warning("No results found")
    
    elif mode == "🧰 Tools":
        st.subheader("Available Tools")
        
        tools_info = agent.tools.get_all_tools_info()
        st.code(tools_info, language="text")
        
        # Tool executor
        st.subheader("Execute Tool")
        tool_name = st.selectbox(
            "Select tool:",
            ["calculator", "get_time", "get_date", "search_files", "open_file"]
        )
        
        if tool_name == "calculator":
            expr = st.text_input("Expression:", "2 + 2 * 3")
            if st.button("Calculate"):
                result = agent.tools.execute("calculator", expression=expr)
                st.success(result['result'])
        
        elif tool_name == "search_files":
            pattern = st.text_input("File pattern:", "*.pdf")
            directory = st.text_input("Directory:", "~")
            if st.button("Search"):
                result = agent.tools.execute("search_files", pattern=pattern, directory=directory)
                st.write(result['result'])
        
        elif tool_name in ["get_time", "get_date"]:
            if st.button("Get"):
                result = agent.tools.execute(tool_name)
                st.success(result['result'])
    
    elif mode == "📊 Memory":
        st.subheader("Conversation Memory")
        
        memory = agent.get_memory()
        
        if not memory:
            st.info("No conversation history yet")
        else:
            st.write(f"Total exchanges: {len(memory) // 2}")
            
            for i, msg in enumerate(memory):
                role = "👤 You" if msg['role'] == 'user' else "🤖 Jonty"
                timestamp = msg.get('timestamp', 'N/A')
                
                with st.expander(f"{role} - {timestamp}"):
                    st.write(msg['content'])
    
    elif mode == "⚙️ Config":
        st.subheader("Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Model Settings**")
            st.write(f"Model: {config.get('model', {}).get('name', 'N/A')}")
            st.write(f"Max Tokens: {config.get('model', {}).get('max_tokens', 512)}")
            st.write(f"Temperature: {config.get('model', {}).get('temperature', 0.7)}")
        
        with col2:
            st.write("**Embedding Settings**")
            st.write(f"Model: {config.get('embedding', {}).get('model_name', 'N/A')}")
            st.write(f"Chunk Size: {config.get('chunk_size', 500)}")
            st.write(f"Chunk Overlap: {config.get('chunk_overlap', 50)}")
        
        st.write("**Indexed Paths**")
        for path in config.get('paths', []):
            st.write(f"- {path}")

if __name__ == "__main__":
    main()
