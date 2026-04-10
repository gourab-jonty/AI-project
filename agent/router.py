"""
Jonty Agent - Decision Router
Coordinates between RAG, LLM Brain, and Tools
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)


class Agent:
    """
    Jonty Agent - Main coordinator
    Decides: Search files? Use tools? Answer directly?
    """
    
    def __init__(self, brain, tools, retriever):
        """
        Initialize Agent
        
        Args:
            brain: Brain module (LLM inference)
            tools: Tools module (actions)
            retriever: Retriever module (file search)
        """
        self.brain = brain
        self.tools = tools
        self.retriever = retriever
        
        # Conversation memory (last 10 exchanges)
        self.memory = []
        self.max_memory = 10
        
        logger.info("Agent initialized")
    
    def process_query(self, query: str, search_files: bool = True) -> Dict[str, Any]:
        """
        Main entry point - process user query
        
        Args:
            query: User's question/command
            search_files: Whether to search local files
            
        Returns:
            Response dict with: response, thoughts, tool_used, context, etc.
        """
        
        logger.info(f"Query: {query}")
        
        # Step 1: Decision Making
        decisions = self._make_decisions(query)
        logger.info(f"Decisions: {decisions}")
        
        # Step 2: Get context if needed
        context = ""
        if decisions['should_search_files'] and search_files:
            context = self._search_and_retrieve(query)
            logger.info(f"Retrieved context: {len(context)} chars")
        
        # Step 3: Generate response with LLM
        tools_info = self.tools.get_all_tools_info() if decisions['should_consider_tools'] else None
        
        response_data = self.brain.generate_response(
            query=query,
            context=context,
            tools_info=tools_info,
            memory=self.memory
        )
        
        # Step 4: Check if tool call needed
        tool_result = None
        if response_data.get('tool_call'):
            tool_result = self._execute_tool(response_data['tool_call'])
            
            # If tool executed, regenerate response with tool result
            if tool_result.get('success'):
                response_data['tool_result'] = tool_result
                logger.info(f"Tool executed: {tool_result}")
        
        # Step 5: Update memory
        self._update_memory(query, response_data.get('response', ''))
        
        # Step 6: Prepare final output
        result = {
            'success': True,
            'query': query,
            'response': response_data.get('response', ''),
            'context_used': bool(context),
            'tool_used': response_data.get('tool_call') is not None,
            'tool_result': tool_result,
            'confidence': response_data.get('confidence', 0.7),
            'timestamp': datetime.now().isoformat(),
        }
        
        logger.info(f"Response: {result['response'][:100]}...")
        return result
    
    def _make_decisions(self, query: str) -> Dict[str, bool]:
        """
        Decide what actions to take
        
        Returns:
            decisions dict with flags
        """
        query_lower = query.lower()
        
        return {
            'should_search_files': self.brain.is_question_about_files(query),
            'should_consider_tools': self.brain.is_tool_request(query),
            'is_greeting': any(w in query_lower for w in ['hello', 'hi', 'hey', 'good morning']),
            'requires_real_time': any(w in query_lower for w in ['now', 'current', 'today', 'weather', 'time']),
        }
    
    def _search_and_retrieve(self, query: str) -> str:
        """
        Search files and build context
        
        Returns:
            Context string
        """
        try:
            # Search for relevant documents
            results = self.retriever.search(query, top_k=5)
            
            if not results:
                return "No relevant documents found."
            
            # Build context
            context = "RETRIEVED CONTEXT:\n"
            for i, (doc_id, score, content) in enumerate(results, 1):
                # Summarize if too long
                if len(content) > 500:
                    content = self.brain.summarize(content, max_length=500)
                
                context += f"\n[Document {i}] (relevance: {score:.2%})\n{content}\n"
            
            return context
        except Exception as e:
            logger.error(f"Retrieval error: {e}")
            return ""
    
    def _execute_tool(self, tool_call: Dict) -> Dict[str, Any]:
        """
        Execute a tool call
        
        Args:
            tool_call: Tool call dict with 'tool' and 'args'
            
        Returns:
            Tool execution result
        """
        try:
            tool_name = tool_call.get('tool')
            args = tool_call.get('args', {})
            
            logger.info(f"Executing tool: {tool_name} with args: {args}")
            
            result = self.tools.execute(tool_name, **args)
            return result
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _update_memory(self, query: str, response: str):
        """Update conversation memory"""
        self.memory.append({
            'role': 'user',
            'content': query,
            'timestamp': datetime.now().isoformat()
        })
        
        self.memory.append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last N exchanges
        if len(self.memory) > self.max_memory * 2:
            self.memory = self.memory[-(self.max_memory * 2):]
    
    def get_memory(self) -> List[Dict]:
        """Get conversation history"""
        return self.memory
    
    def clear_memory(self):
        """Clear conversation history"""
        self.memory = []
        logger.info("Memory cleared")
    
    def explain_thinking(self, query: str) -> Dict[str, Any]:
        """
        Explain the agent's thinking process
        Useful for debugging
        """
        decisions = self._make_decisions(query)
        
        reasoning = []
        if decisions['should_search_files']:
            reasoning.append("🔍 Will search local files")
        if decisions['should_consider_tools']:
            reasoning.append("🧰 Will consider using tools")
        if decisions['is_greeting']:
            reasoning.append("👋 Detected greeting")
        if decisions['requires_real_time']:
            reasoning.append("⏰ Requires real-time information")
        
        return {
            'query': query,
            'decisions': decisions,
            'reasoning': reasoning,
        }
