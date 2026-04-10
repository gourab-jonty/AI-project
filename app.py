"""
Jonty - Unified Web UI
Single Streamlit dashboard for all 5 agents
"""

import streamlit as st
import os
import sys
import time
import yaml
from datetime import datetime
from pathlib import Path

# Add project root
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents import UnifiedAgentManager
from agent.brain import Brain

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Jonty - AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

with st.sidebar:
    st.title("🤖 Jonty")
    st.markdown("---")
    st.markdown("**Offline Personal AI Assistant**")
    st.markdown("---")
    
    page = st.radio(
        "Choose Mode:",
        ["💬 Chat", "🧠 Enhanced Reasoning", "🔗 Integrations", "📊 Analytics", "⚙️ Settings"],
        index=0
    )

# Initialize session
if 'brain' not in st.session_state:
    # Load config
    config_path = project_root / "config.yaml"
    if not config_path.exists():
        config_path = project_root / "config-highend.yaml"
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    st.session_state.brain = Brain(config)
    st.session_state.brain.load_model()  # Load the LLM model
    st.session_state.manager = UnifiedAgentManager(st.session_state.brain)

manager = st.session_state.manager
brain = st.session_state.brain

# ============================================================================
# PAGE: CHAT MODE
# ============================================================================

if page == "💬 Chat":
    st.header("💬 Chat with Jonty")
    st.markdown("Have a natural conversation. I'll help with questions, explanations, and advice.")
    st.markdown("---")
    
    # Chat interface
    col1, col2 = st.columns([0.85, 0.15])
    
    with col1:
        user_input = st.text_input(
            "Your message:",
            placeholder="Ask me anything...",
            key="chat_input"
        )
    
    with col2:
        if st.button("Send 📤", use_container_width=True):
            if user_input:
                with st.spinner("Thinking..."):
                    response_obj = manager.process_query(user_input, mode='chat')
                    result = response_obj['result']
                    
                    # Display response
                    st.success(f"✅ Response in {response_obj['execution_time']}")
                    st.write(f"**Jonty:** {result['response']}")
                    
                    # Store in session
                    if 'chat_history' not in st.session_state:
                        st.session_state.chat_history = []
                    
                    st.session_state.chat_history.append({
                        'user': user_input,
                        'assistant': result['response']
                    })
    
    st.markdown("---")
    
    # Display chat history
    if 'chat_history' in st.session_state and st.session_state.chat_history:
        st.subheader("📜 Conversation History")
        for msg in st.session_state.chat_history[-5:]:
            st.markdown(f"**You:** {msg['user']}")
            st.markdown(f"**Jonty:** {msg['assistant']}")
            st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear History 🗑️", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

# ============================================================================
# PAGE: ENHANCED REASONING
# ============================================================================

elif page == "🧠 Enhanced Reasoning":
    st.header("🧠 Advanced Problem Solving")
    st.markdown("For complex multi-step questions, comparisons, calculations, and analysis.")
    st.markdown("---")
    
    col1, col2 = st.columns([0.85, 0.15])
    
    with col1:
        complex_query = st.text_area(
            "Your complex question:",
            placeholder="E.g., 'Compare X and Y, then summarize the differences'",
            height=100,
            key="complex_query"
        )
    
    with col2:
        if st.button("Analyze 🔍", use_container_width=True):
            if complex_query:
                with st.spinner("Analyzing..."):
                    response_obj = manager.process_query(complex_query, mode='enhanced')
                    result = response_obj['result']
                    
                    # Display analysis
                    st.success(f"✅ Analysis in {response_obj['execution_time']}")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Complexity", f"{result['complexity']:.1%}")
                    with col2:
                        st.metric("Steps", result['steps'])
                    with col3:
                        st.metric("Status", "Complete")
                    
                    st.subheader("Final Answer:")
                    st.info(result['final_response'])
                    
                    st.subheader("Reasoning Process:")
                    for i, step_result in enumerate(result['results'], 1):
                        st.write(f"**Step {i}:** {step_result['action']} → {step_result['status']}")
    
    st.markdown("---")
    st.info("💡 Use this for tasks requiring reasoning, multiple steps, or synthesis of information.")

# ============================================================================
# PAGE: INTEGRATIONS
# ============================================================================

elif page == "🔗 Integrations":
    st.header("🔗 External Services")
    st.markdown("Connect with weather, calendar, email, and web search services.")
    st.markdown("---")
    
    # Available services
    services = manager.integration.get_available_services()
    
    st.subheader("Available Services:")
    cols = st.columns(len(services))
    for col, service in zip(cols, services):
        with col:
            st.button(f"📌 {service.title()}", use_container_width=True, disabled=True)
    
    st.markdown("---")
    
    # Query with integrations
    integration_query = st.text_input(
        "Ask about services:",
        placeholder="E.g., 'What's the weather?' or 'Show my calendar'",
        key="integration_query"
    )
    
    if st.button("Query Services 🔄", use_container_width=True):
        if integration_query:
            with st.spinner("Fetching..."):
                response_obj = manager.process_query(integration_query, mode='integration')
                result = response_obj['result']
                
                st.success(f"✅ Fetched in {response_obj['execution_time']}")
                
                if result['services_used']:
                    st.subheader("Service Results:")
                    for service, data in result['results'].items():
                        with st.expander(f"📊 {service.title()}"):
                            st.write(data['data'])
                else:
                    st.info("No services matched your query. Try asking about weather, calendar, or email.")
    
    st.markdown("---")
    st.info("🔌 Services shown are mock implementations. Configure real APIs in settings.")

# ============================================================================
# PAGE: ANALYTICS
# ============================================================================

elif page == "📊 Analytics":
    st.header("📊 Performance Analytics")
    st.markdown("Track usage, performance metrics, and insights.")
    st.markdown("---")
    
    # Stats
    stats = manager.get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Queries", stats['total_queries'])
    with col2:
        st.metric("Chat Turns", stats['chat_turns'])
    with col3:
        perf = stats['performance']
        st.metric("Avg Time", perf.get('avg_time', 'N/A'))
    with col4:
        st.metric("Best Time", perf.get('min_time', 'N/A'))
    
    st.markdown("---")
    
    # Trending
    trending = stats['trending']
    if trending:
        st.subheader("🔥 Trending Queries:")
        for i, query in enumerate(trending, 1):
            st.write(f"{i}. {query}")
    else:
        st.info("No queries yet")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Export Report"):
            manager.export_report()
            st.success("✅ Report exported to `jonty_report.json`")
    
    with col2:
        if st.button("🔄 Reset Analytics"):
            manager.reset_all()
            st.success("✅ All agents reset")
    
    with col3:
        if st.button("📊 Generate HTML Report"):
            manager.analytics.generate_html_report()
            st.success("✅ Report saved to `report.html`")

# ============================================================================
# PAGE: SETTINGS
# ============================================================================

elif page == "⚙️ Settings":
    st.header("⚙️ Settings & Configuration")
    st.markdown("---")
    
    # Agent info
    st.subheader("🤖 Available Agents:")
    agents_info = manager.get_agent_info()
    for agent, description in agents_info.items():
        st.write(f"**{agent.replace('_', ' ').title()}:** {description}")
    
    st.markdown("---")
    
    # Model info
    st.subheader("🧠 Model Configuration:")
    
    try:
        config = brain.config
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Model", config.get('brain_model', 'TinyLlama'))
            st.metric("Embedding Model", config.get('embedding_model', 'all-MiniLM-L6-v2'))
        
        with col2:
            st.metric("Max Tokens", config.get('max_output_tokens', 512))
            st.metric("Chunk Size", config.get('chunk_size', 500))
    except Exception as e:
        st.warning(f"Could not load config: {e}")
    
    st.markdown("---")
    
    # About
    st.subheader("ℹ️ About Jonty")
    st.markdown("""
    **Jonty** is an offline personal AI assistant featuring:
    - 🔍 File search with FAISS vector database
    - 🧠 Offline LLM (TinyLlama) for local processing
    - 🛠️ 9+ built-in tools (calculator, weather, calendar, etc.)
    - 🤖 5 specialized agents (Chat, Enhanced, Integration, Analytics, Web UI)
    - 🖥️ Cross-platform support (Windows, macOS, Linux)
    
    **Privacy First:** Everything runs offline on your machine. No data sent to external servers.
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
Made with ❤️ by Jonty Team | v1.0.0
</div>
""", unsafe_allow_html=True)
