"""
Jonty - All 5 Agents in ONE File
Unified agent system for Streamlit Web UI
"""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
import statistics
import time

logger = logging.getLogger(__name__)


# ============================================================================
# 1. ENHANCED AGENT - Complex Reasoning
# ============================================================================

class EnhancedAgent:
    """Advanced reasoning & multi-step problem solving"""
    
    def __init__(self, base_agent):
        self.base_agent = base_agent
        self.reasoning_depth = 3
        self.max_steps = 5
        logger.info("Enhanced Agent ready")
    
    def process_complex_query(self, query: str) -> Dict[str, Any]:
        """Process with multi-step reasoning"""
        complexity = self._analyze_complexity(query)
        
        if complexity > 0.5:
            steps = self._plan_steps(query)
        else:
            steps = [{"step": 1, "action": "direct_answer", "query": query}]
        
        results = [self._execute_step(step, i, len(steps)) for i, step in enumerate(steps, 1)]
        final_response = self._synthesize_results(results, query)
        
        return {
            'query': query,
            'complexity': complexity,
            'steps': len(steps),
            'results': results,
            'final_response': final_response
        }
    
    def _analyze_complexity(self, query: str) -> float:
        """Analyze query complexity (0-1)"""
        query_lower = query.lower()
        score = 0.0
        
        keywords = {
            'and|also|besides|,|;': 0.2,
            'if|when|unless|given': 0.2,
            'compare|difference|vs': 0.2,
            'summarize|total|count': 0.15,
            'analyze|explain|why|how': 0.15
        }
        
        for pattern, points in keywords.items():
            if any(w in query_lower for w in pattern.split('|')):
                score += points
        
        return min(score, 1.0)
    
    def _plan_steps(self, query: str) -> List[Dict]:
        """Break into steps"""
        steps = []
        query_lower = query.lower()
        
        if any(w in query_lower for w in ['search', 'find']):
            steps.append({"step": len(steps)+1, "action": "search", "query": query})
        if any(w in query_lower for w in ['calculate', '+', '-', '*']):
            steps.append({"step": len(steps)+1, "action": "calculate", "query": query})
        if any(w in query_lower for w in ['summarize', 'explain']):
            steps.append({"step": len(steps)+1, "action": "synthesize", "query": query})
        
        return steps if steps else [{"step": 1, "action": "answer", "query": query}]
    
    def _execute_step(self, step: Dict, step_num: int, total: int) -> Dict:
        """Execute single step"""
        return {
            "step": step_num,
            "action": step.get('action'),
            "status": "completed"
        }
    
    def _synthesize_results(self, results: List[Dict], query: str) -> str:
        """Synthesize all results"""
        return f"Completed {len(results)} steps for your query"


# ============================================================================
# 2. CHAT AGENT - Conversational
# ============================================================================

class ChatAgent:
    """Advanced conversational management"""
    
    def __init__(self, base_agent):
        self.base_agent = base_agent
        self.conversation_history = deque(maxlen=50)
        self.topics = []
        logger.info("Chat Agent ready")
    
    def chat(self, user_message: str) -> Dict[str, Any]:
        """Process chat message"""
        intent = self._extract_intent(user_message)
        
        if intent['type'] == 'greeting':
            response = "Hello! 👋 I'm Jonty. How can I help you today?"
        else:
            response_obj = self.base_agent.generate_response(user_message)
            response = response_obj.get('response', 'I couldn\'t understand that')
        
        self.conversation_history.append({
            'user': user_message,
            'assistant': response,
            'intent': intent['type'],
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'response': response,
            'intent': intent['type'],
            'turn': len(self.conversation_history),
            'suggested_follow_ups': self._suggest_follow_ups(user_message)
        }
    
    def _extract_intent(self, message: str) -> Dict:
        """Extract user intent"""
        msg_lower = message.lower()
        
        intents = {
            'greeting': ['hello', 'hi', 'hey', 'good morning'],
            'clarification': ['what do you mean', 'explain', 'clarify'],
            'follow_up': ['more', 'add', 'also', 'furthermore']
        }
        
        for intent_type, keywords in intents.items():
            if any(k in msg_lower for k in keywords):
                return {'type': intent_type, 'confidence': 0.9}
        
        return {'type': 'general', 'confidence': 0.5}
    
    def get_history(self) -> str:
        """Get formatted conversation history"""
        if not self.conversation_history:
            return "No conversation yet"
        
        history = "📜 Conversation History:\n"
        for msg in list(self.conversation_history)[-10:]:
            history += f"👤 You: {msg['user'][:50]}...\n"
            history += f"🤖 Jonty: {msg['assistant'][:50]}...\n\n"
        
        return history
    
    def _suggest_follow_ups(self, message: str) -> List[str]:
        """Suggest follow-up questions"""
        return ["Tell me more", "Can you explain further?", "Any other suggestions?"]
    
    def reset(self):
        """Clear conversation"""
        self.conversation_history.clear()


# ============================================================================
# 3. INTEGRATION AGENT - External Services
# ============================================================================

class IntegrationAgent:
    """External API & service integration"""
    
    def __init__(self):
        self.services = {}
        self.log = []
        logger.info("Integration Agent ready")
    
    def process_integrated_query(self, query: str) -> Dict[str, Any]:
        """Process query with integrations"""
        query_lower = query.lower()
        
        results = {}
        
        if any(w in query_lower for w in ['weather', 'rain', 'temperature']):
            results['weather'] = {
                'status': 'success',
                'data': 'Weather: Sunny, 72°F (Mock)'
            }
        
        if any(w in query_lower for w in ['calendar', 'meeting', 'schedule']):
            results['calendar'] = {
                'status': 'success',
                'data': 'Calendar: 2 meetings today (Mock)'
            }
        
        if any(w in query_lower for w in ['email', 'mail', 'inbox']):
            results['email'] = {
                'status': 'success',
                'data': '3 unread emails (Mock)'
            }
        
        return {
            'query': query,
            'services_used': list(results.keys()),
            'results': results
        }
    
    def get_available_services(self) -> List[str]:
        """List available services"""
        return ['weather', 'calendar', 'email', 'web_search']


# ============================================================================
# 4. ANALYTICS AGENT - Performance Tracking
# ============================================================================

class AnalyticsAgent:
    """Performance tracking & insights"""
    
    def __init__(self):
        self.queries = []
        self.exec_times = []
        self.errors = []
        self.session_start = datetime.now()
        logger.info("Analytics Agent ready")
    
    def log_query(self, query: str, execution_time: float, tool_used: Optional[str] = None) -> None:
        """Log query"""
        self.queries.append({
            'query': query,
            'time': execution_time,
            'tool': tool_used,
            'timestamp': datetime.now().isoformat()
        })
        self.exec_times.append(execution_time)
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance stats"""
        if not self.exec_times:
            return {'status': 'no_data'}
        
        return {
            'total_queries': len(self.queries),
            'avg_time': f"{statistics.mean(self.exec_times):.2f}s",
            'min_time': f"{min(self.exec_times):.2f}s",
            'max_time': f"{max(self.exec_times):.2f}s",
            'median_time': f"{statistics.median(self.exec_times):.2f}s"
        }
    
    def get_trending_queries(self, top_n: int = 5) -> List[str]:
        """Get trending queries"""
        from collections import Counter
        queries = [q['query'] for q in self.queries]
        return [item[0] for item in Counter(queries).most_common(top_n)]
    
    def generate_html_report(self, filepath: str = 'report.html') -> bool:
        """Generate HTML report"""
        perf = self.get_performance_summary()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Jonty Analytics</title>
            <style>
                body {{ font-family: Arial; margin: 20px; }}
                .metric {{ background: #f0f2f6; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                h1 {{ color: #1f77b4; }}
            </style>
        </head>
        <body>
            <h1>📊 Jonty Analytics Report</h1>
            <div class="metric">
                <p><strong>Total Queries:</strong> {perf.get('total_queries', 0)}</p>
                <p><strong>Avg Time:</strong> {perf.get('avg_time', 'N/A')}</p>
                <p><strong>Best Time:</strong> {perf.get('min_time', 'N/A')}</p>
            </div>
        </body>
        </html>
        """
        
        with open(filepath, 'w') as f:
            f.write(html)
        
        return True


# ============================================================================
# 5. UNIFIED AGENT MANAGER
# ============================================================================

class UnifiedAgentManager:
    """Master agent managing all 5 agents"""
    
    def __init__(self, base_agent):
        self.base_agent = base_agent
        
        # Initialize all agents
        self.enhanced = EnhancedAgent(base_agent)
        self.chat = ChatAgent(base_agent)
        self.integration = IntegrationAgent()
        self.analytics = AnalyticsAgent()
        
        logger.info("✅ All 5 Agents initialized!")
    
    def process_query(self, query: str, mode: str = 'auto') -> Dict[str, Any]:
        """
        Process query using appropriate agent
        
        Args:
            query: User query
            mode: 'auto', 'enhanced', 'chat', 'integration', 'analytics'
        
        Returns:
            Response from appropriate agent
        """
        
        start = time.time()
        
        # Auto-select agent
        if mode == 'auto':
            mode = self._select_agent(query)
        
        # Route to agent
        if mode == 'enhanced':
            result = self.enhanced.process_complex_query(query)
        elif mode == 'chat':
            result = self.chat.chat(query)
        elif mode == 'integration':
            result = self.integration.process_integrated_query(query)
        else:
            result = self.base_agent.generate_response(query)
        
        # Log to analytics
        exec_time = time.time() - start
        self.analytics.log_query(query, exec_time)
        
        return {
            'mode': mode,
            'result': result,
            'execution_time': f"{exec_time:.2f}s"
        }
    
    def _select_agent(self, query: str) -> str:
        """Auto-select best agent"""
        query_lower = query.lower()
        
        if any(w in query_lower for w in ['weather', 'calendar', 'email']):
            return 'integration'
        if any(w in query_lower for w in ['and', 'compare', 'analyze', 'calculate']):
            return 'enhanced'
        if any(w in query_lower for w in [',', 'tell me', 'explain']):
            return 'chat'
        
        return 'default'
    
    def get_agent_info(self) -> Dict[str, str]:
        """Get all agents info"""
        return {
            'enhanced': 'Complex reasoning & multi-step tasks',
            'chat': 'Natural conversation with context',
            'integration': 'External APIs & services',
            'analytics': 'Performance tracking & insights',
            'web_ui': 'Beautiful Streamlit interface'
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get unified statistics"""
        return {
            'total_queries': len(self.analytics.queries),
            'chat_turns': len(self.chat.conversation_history),
            'performance': self.analytics.get_performance_summary(),
            'trending': self.analytics.get_trending_queries(5)
        }
    
    def reset_all(self):
        """Reset all agents"""
        self.chat.reset()
        self.analytics = AnalyticsAgent()
        logger.info("All agents reset")
    
    def export_report(self, filepath: str = 'jonty_report.json') -> bool:
        """Export full report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'statistics': self.get_stats(),
            'trending_queries': self.analytics.get_trending_queries(10),
            'conversation': list(self.chat.conversation_history)
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        return True


# ============================================================================
# QUICK START
# ============================================================================

def create_unified_manager(base_agent):
    """Factory function"""
    return UnifiedAgentManager(base_agent)
