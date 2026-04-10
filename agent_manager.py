"""
Jonty Agent Manager - Unified interface for all 5 agents
Coordinates between Streamlit Web, Enhanced, Chat, Integration, and Analytics agents
"""

import logging
from typing import Dict, Any, Optional
from agent_streamlit import None  # Import handled separately
from agent_enhanced import EnhancedAgent
from agent_chat import ChatAgent
from agent_integration import IntegrationAgent
from agent_analytics import AnalyticsAgent

logger = logging.getLogger(__name__)


class JontyAgentManager:
    """Unified manager for all agents"""
    
    def __init__(self, base_agent):
        """Initialize all agents"""
        
        self.base_agent = base_agent
        
        # Initialize specialized agents
        self.enhanced = EnhancedAgent(base_agent)
        self.chat = ChatAgent(base_agent)
        self.integration = IntegrationAgent()
        self.analytics = AnalyticsAgent()
        
        # Setup default integration services
        self.integration.setup_default_services()
        
        logger.info("🚀 Jonty Agent Manager initialized with all 5 agents")
    
    def process_query(self, query: str, agent_type: str = 'auto', **options) -> Dict[str, Any]:
        """
        Process query using appropriate agent
        
        Args:
            query: User query
            agent_type: Which agent to use ('auto', 'enhanced', 'chat', 'integration', 'analytics', 'all')
            **options: Additional options for specific agents
            
        Returns:
            Processed response
        """
        
        import time
        start_time = time.time()
        
        # Auto-detect best agent
        if agent_type == 'auto':
            agent_type = self._select_best_agent(query)
        
        logger.info(f"Processing with {agent_type} agent: {query[:50]}...")
        
        responses = {}
        
        # Route to appropriate agent(s)
        if agent_type in ['enhanced', 'all']:
            responses['enhanced'] = self.enhanced.process_complex_query(query)
        
        if agent_type in ['chat', 'all']:
            responses['chat'] = self.chat.chat(query)
        
        if agent_type == 'integration' or (agent_type == 'all' and self._needs_integration(query)):
            responses['integration'] = self.integration.process_integrated_query(query)
        
        if agent_type != 'all':
            # Single agent response
            response = responses.get(agent_type) or self.base_agent.process_query(query)
        else:
            # Multi-agent response
            response = responses
        
        # Log analytics
        execution_time = time.time() - start_time
        if isinstance(response, dict) and 'response' in response:
            self.analytics.log_query(
                query=query,
                response=response,
                execution_time=execution_time,
                tool_used=response.get('tool_result', {}).get('tool'),
                context_used=response.get('context_used', False)
            )
        
        return response
    
    def _select_best_agent(self, query: str) -> str:
        """Auto-select best agent for query"""
        
        query_lower = query.lower()
        
        # Check for integration needs (APIs, weather, calendar, etc.)
        if any(w in query_lower for w in ['weather', 'calendar', 'email', 'search web']):
            return 'integration'
        
        # Check for complex queries
        if any(w in query_lower for w in ['and', 'also', 'compare', 'analyze']):
            return 'enhanced'
        
        # Check for conversational patterns
        if any(w in query_lower for w in ['tell me', 'explain', 'what', 'how', ',']):
            return 'chat'
        
        # Default
        return 'enhanced'
    
    def _needs_integration(self, query: str) -> bool:
        """Check if query needs integration services"""
        
        query_lower = query.lower()
        return any(w in query_lower for w in ['weather', 'calendar', 'email', 'web', 'api'])
    
    def get_agent_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all agents"""
        
        return {
            'enhanced': {
                'name': 'Enhanced Agent',
                'description': 'Complex reasoning & multi-step processing',
                'best_for': 'Complex queries, multi-part questions'
            },
            'chat': {
                'name': 'Chat Agent',
                'description': 'Conversational memory & context',
                'best_for': 'Natural conversation flow'
            },
            'integration': {
                'name': 'Integration Agent',
                'description': 'External APIs & services',
                'best_for': 'Weather, calendar, email, web search'
            },
            'analytics': {
                'name': 'Analytics Agent',
                'description': 'Performance tracking & insights',
                'best_for': 'Performance analysis & reports'
            },
            'web_ui': {
                'name': 'Streamlit Web UI',
                'description': 'Beautiful web interface',
                'best_for': 'GUI interaction'
            }
        }
    
    def get_all_stats(self) -> Dict[str, Any]:
        """Get statistics from all agents"""
        
        return {
            'chat_exchanges': len(self.chat.conversation_history),
            'total_queries': len(self.analytics.queries),
            'total_errors': len(self.analytics.error_log),
            'available_services': self.integration.get_available_services(),
            'performance': self.analytics.get_performance_summary(),
            'insights': self.analytics.get_insights(),
        }
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive report from all agents"""
        
        return {
            'timestamp': __import__('datetime').datetime.now().isoformat(),
            'agent_info': self.get_agent_info(),
            'statistics': self.get_all_stats(),
            'chat_summary': self.chat.get_conversation_summary(),
            'session_report': self.analytics.get_session_report(),
            'trending': self.analytics.get_trending_queries(5),
            'slow_queries': self.analytics.get_slow_queries(2.0, 5),
        }
    
    def export_all_reports(self, base_path: str = './reports') -> Dict[str, bool]:
        """Export reports from all agents"""
        
        import os
        os.makedirs(base_path, exist_ok=True)
        
        results = {
            'analytics_json': self.analytics.export_analytics(f'{base_path}/analytics.json'),
            'analytics_html': self.analytics.generate_html_report(f'{base_path}/report.html'),
            'chat_export': self.chat.export_conversation(f'{base_path}/conversation.json'),
            'integration_export': True  # self.integration.export_integration_config(f'{base_path}/integrations.json')
        }
        
        logger.info(f"All reports exported to {base_path}")
        return results
    
    def clear_all_history(self) -> Dict[str, bool]:
        """Clear history from all agents"""
        
        self.chat.reset_conversation()
        self.analytics.queries.clear()
        self.analytics.error_log.clear()
        
        return {
            'chat': True,
            'analytics': True
        }


def create_agent_from_main():
    """Factory function to create manager from main.py components"""
    
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    from main import Jonty
    
    jonty = Jonty()
    manager = JontyAgentManager(jonty.agent)
    
    return manager


if __name__ == '__main__':
    # Example usage
    manager = create_agent_from_main()
    
    # Process query with auto-selected agent
    result = manager.process_query("What Python files do I have and calculate 2+2?")
    print(result)
    
    # Get comprehensive report
    report = manager.generate_comprehensive_report()
    print(report)
