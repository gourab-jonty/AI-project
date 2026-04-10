"""
Jonty Enhanced Agent - Advanced Reasoning & Multi-Step Tasks
Handles complex queries with planning and reasoning
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class EnhancedAgent:
    """
    Advanced agent with reasoning, planning, and multi-step task execution
    """
    
    def __init__(self, base_agent):
        """
        Initialize Enhanced Agent
        
        Args:
            base_agent: Base Agent instance (from router.py)
        """
        self.base_agent = base_agent
        self.reasoning_depth = 3  # How deep to reason
        self.max_steps = 5        # Max steps in multi-step tasks
        self.task_history = []
        
        logger.info("Enhanced Agent initialized")
    
    def process_complex_query(self, query: str) -> Dict[str, Any]:
        """
        Process complex query with reasoning and planning
        
        Args:
            query: User's complex question
            
        Returns:
            Detailed response with reasoning steps
        """
        
        logger.info(f"Processing complex query: {query}")
        
        # Step 1: Analyze query complexity
        complexity = self._analyze_complexity(query)
        logger.info(f"Complexity score: {complexity}")
        
        # Step 2: Break down into steps
        if complexity > 0.5:
            steps = self._plan_steps(query)
            logger.info(f"Breaking into {len(steps)} steps")
        else:
            steps = [{"step": 1, "action": "direct_answer", "query": query}]
        
        # Step 3: Execute steps
        results = []
        for i, step in enumerate(steps, 1):
            step_result = self._execute_step(step, i, len(steps))
            results.append(step_result)
        
        # Step 4: Synthesize results
        final_response = self._synthesize_results(results, query)
        
        # Step 5: Add reasoning explanation
        response = {
            'success': True,
            'query': query,
            'complexity': complexity,
            'steps_taken': len(steps),
            'step_results': results,
            'final_response': final_response,
            'reasoning': self._explain_reasoning(steps, results),
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Complex query processed: {len(steps)} steps")
        return response
    
    def _analyze_complexity(self, query: str) -> float:
        """
        Analyze query complexity (0.0 = simple, 1.0 = very complex)
        
        Returns:
            Complexity score
        """
        
        query_lower = query.lower()
        complexity = 0.0
        
        # Check for multi-part queries
        if any(w in query_lower for w in ['and', 'also', 'besides', ',', ';']):
            complexity += 0.2
        
        # Check for conditional logic
        if any(w in query_lower for w in ['if', 'when', 'unless', 'given', 'assuming']):
            complexity += 0.2
        
        # Check for comparison
        if any(w in query_lower for w in ['compare', 'difference', 'vs', 'versus', 'similar']):
            complexity += 0.2
        
        # Check for aggregation
        if any(w in query_lower for w in ['summarize', 'total', 'count', 'list all', 'aggregate']):
            complexity += 0.15
        
        # Check for analysis
        if any(w in query_lower for w in ['analyze', 'explain', 'why', 'how', 'pattern']):
            complexity += 0.15
        
        return min(complexity, 1.0)
    
    def _plan_steps(self, query: str) -> List[Dict]:
        """
        Break complex query into steps
        
        Returns:
            List of steps to execute
        """
        
        steps = []
        query_lower = query.lower()
        
        # Determine step types
        if 'search' in query_lower or 'find' in query_lower:
            steps.append({"step": 1, "action": "search", "sub_queries": self._extract_search_queries(query)})
        
        if 'calculate' in query_lower or any(op in query for op in ['+', '-', '*', '/', '%']):
            steps.append({"step": len(steps) + 1, "action": "calculate", "expression": self._extract_expression(query)})
        
        if 'summarize' in query_lower or 'explain' in query_lower:
            steps.append({"step": len(steps) + 1, "action": "synthesize", "context": "retrieved_data"})
        
        if not steps:
            steps.append({"step": 1, "action": "direct_answer", "query": query})
        
        return steps
    
    def _execute_step(self, step: Dict, step_num: int, total_steps: int) -> Dict:
        """Execute a single step"""
        
        action = step.get('action')
        
        try:
            if action == 'search':
                return self._execute_search_step(step)
            elif action == 'calculate':
                return self._execute_calculate_step(step)
            elif action == 'synthesize':
                return self._execute_synthesize_step(step)
            elif action == 'direct_answer':
                return self._execute_answer_step(step)
            else:
                return {
                    "step": step_num,
                    "action": action,
                    "status": "unknown",
                    "result": None
                }
        except Exception as e:
            logger.error(f"Step {step_num} failed: {e}")
            return {
                "step": step_num,
                "action": action,
                "status": "failed",
                "error": str(e)
            }
    
    def _execute_search_step(self, step: Dict) -> Dict:
        """Execute search step"""
        
        sub_queries = step.get('sub_queries', [])
        results = []
        
        for query in sub_queries:
            search_result = self.base_agent.retriever.search(query, top_k=3)
            results.append({
                "query": query,
                "results": search_result
            })
        
        return {
            "action": "search",
            "status": "success",
            "queries_processed": len(sub_queries),
            "results": results
        }
    
    def _execute_calculate_step(self, step: Dict) -> Dict:
        """Execute calculation step"""
        
        expression = step.get('expression', '')
        result = self.base_agent.tools.execute('calculator', expression=expression)
        
        return {
            "action": "calculate",
            "status": "success" if result.get('success') else 'failed',
            "expression": expression,
            "result": result.get('result', 'N/A')
        }
    
    def _execute_synthesize_step(self, step: Dict) -> Dict:
        """Execute synthesis step"""
        
        return {
            "action": "synthesize",
            "status": "success",
            "synthesis": "Data synthesized from previous steps"
        }
    
    def _execute_answer_step(self, step: Dict) -> Dict:
        """Execute direct answer step"""
        
        query = step.get('query', '')
        response = self.base_agent.brain.generate_response(query)
        
        return {
            "action": "direct_answer",
            "status": "success",
            "response": response.get('response', 'No response')
        }
    
    def _extract_search_queries(self, query: str) -> List[str]:
        """Extract individual search queries from complex query"""
        
        # Simple extraction: split by 'and'
        parts = query.split(' and ')
        return [p.strip() for p in parts if p.strip()]
    
    def _extract_expression(self, query: str) -> str:
        """Extract mathematical expression from query"""
        
        import re
        expr_pattern = r'[\d\s+\-*/()%]+'
        match = re.search(expr_pattern, query)
        return match.group(0).strip() if match else ''
    
    def _synthesize_results(self, results: List[Dict], query: str) -> str:
        """Synthesize all results into final answer"""
        
        synthesis = "Based on the analysis:\n\n"
        
        for i, result in enumerate(results, 1):
            action = result.get('action')
            status = result.get('status')
            
            if action == 'search' and status == 'success':
                synthesis += f"• Found relevant documents\n"
            elif action == 'calculate' and status == 'success':
                synthesis += f"• Calculation result: {result.get('result')}\n"
            elif action == 'direct_answer' and status == 'success':
                synthesis += f"• {result.get('response')}\n"
        
        return synthesis
    
    def _explain_reasoning(self, steps: List[Dict], results: List[Dict]) -> str:
        """Explain the reasoning process"""
        
        explanation = "Reasoning Process:\n"
        explanation += f"1. Identified {len(steps)} steps to solve the query\n"
        
        for i, (step, result) in enumerate(zip(steps, results), 1):
            action = step.get('action')
            status = result.get('status')
            explanation += f"{i+1}. {action} step: {status}\n"
        
        return explanation
    
    def explain_thinking(self, query: str) -> Dict[str, Any]:
        """Explain the agent's thinking in detail"""
        
        steps = self._plan_steps(query)
        complexity = self._analyze_complexity(query)
        
        return {
            'query': query,
            'complexity_score': complexity,
            'planned_steps': len(steps),
            'step_breakdown': steps,
            'reasoning': self._explain_reasoning(steps, []),
        }
    
    def get_task_history(self) -> List[Dict]:
        """Get history of completed tasks"""
        
        return self.task_history
    
    def save_reasoning_trace(self, response: Dict, filepath: str = 'reasoning_trace.json'):
        """Save detailed reasoning trace for analysis"""
        
        with open(filepath, 'w') as f:
            json.dump(response, f, indent=2, default=str)
        
        logger.info(f"Reasoning trace saved to {filepath}")
