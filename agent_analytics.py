"""
Jonty Analytics Agent - Performance Tracking & Insights
Tracks queries, performance metrics, and generates insights
"""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import statistics

logger = logging.getLogger(__name__)


class AnalyticsAgent:
    """Advanced analytics and performance tracking"""
    
    def __init__(self):
        self.queries = []  # All queries
        self.performance_metrics = defaultdict(list)
        self.user_patterns = defaultdict(int)
        self.error_log = []
        self.session_start = datetime.now()
        
        logger.info("Analytics Agent initialized")
    
    def log_query(self, query: str, response: Dict[str, Any], execution_time: float,
                  tool_used: Optional[str] = None, context_used: bool = False) -> None:
        """Log query execution"""
        
        self.queries.append({
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'execution_time': execution_time,
            'tool_used': tool_used,
            'context_used': context_used,
            'success': response.get('success', False),
            'response_length': len(response.get('response', '')),
            'confidence': response.get('confidence', 0.0)
        })
        
        # Track metrics
        self.performance_metrics['execution_times'].append(execution_time)
        self.performance_metrics['query_count'] += 1
        
        # Track tool usage
        if tool_used:
            self.user_patterns[f'tool_{tool_used}'] += 1
        
        # Track context usage
        if context_used:
            self.user_patterns['file_searches'] += 1
        
        logger.debug(f"Query logged: {query[:50]}... (time: {execution_time:.2f}s)")
    
    def log_error(self, error: str, context: Optional[Dict] = None) -> None:
        """Log error"""
        
        self.error_log.append({
            'error': error,
            'context': context or {},
            'timestamp': datetime.now().isoformat()
        })
        
        logger.error(f"Error logged: {error}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        
        if not self.queries:
            return {'status': 'no_data'}
        
        exec_times = self.performance_metrics['execution_times']
        
        return {
            'total_queries': len(self.queries),
            'avg_execution_time': statistics.mean(exec_times),
            'min_execution_time': min(exec_times),
            'max_execution_time': max(exec_times),
            'median_execution_time': statistics.median(exec_times),
            'std_dev': statistics.stdev(exec_times) if len(exec_times) > 1 else 0,
            'success_rate': sum(1 for q in self.queries if q['success']) / len(self.queries),
            'avg_response_length': statistics.mean([q['response_length'] for q in self.queries]),
            'total_errors': len(self.error_log)
        }
    
    def get_usage_patterns(self) -> Dict[str, Any]:
        """Analyze usage patterns"""
        
        patterns = {
            'most_used_tools': self._get_top_items('tool_', 5),
            'file_searches': self.user_patterns.get('file_searches', 0),
            'total_interactions': len(self.queries),
            'query_types': self._categorize_queries(),
        }
        
        return patterns
    
    def get_trending_queries(self, top_n: int = 5) -> List[Dict]:
        """Get trending/repeated queries"""
        
        query_freq = defaultdict(int)
        for q in self.queries:
            query_freq[q['query']] += 1
        
        trending = sorted(query_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
        
        return [
            {'query': q[0], 'frequency': q[1]}
            for q in trending
        ]
    
    def get_slow_queries(self, threshold: float = 2.0, top_n: int = 5) -> List[Dict]:
        """Get slow queries (above threshold)"""
        
        slow = [q for q in self.queries if q['execution_time'] > threshold]
        slow.sort(key=lambda x: x['execution_time'], reverse=True)
        
        return slow[:top_n]
    
    def get_session_report(self) -> Dict[str, Any]:
        """Generate session report"""
        
        session_duration = datetime.now() - self.session_start
        
        return {
            'session_start': self.session_start.isoformat(),
            'session_duration_seconds': session_duration.total_seconds(),
            'session_duration_formatted': str(session_duration),
            'total_queries': len(self.queries),
            'total_errors': len(self.error_log),
            'performance': self.get_performance_summary(),
            'usage_patterns': self.get_usage_patterns(),
        }
    
    def get_insights(self) -> Dict[str, List[str]]:
        """Generate actionable insights"""
        
        insights = {'recommendations': [], 'warnings': []}
        
        if not self.queries:
            return insights
        
        perf = self.get_performance_summary()
        patterns = self.get_usage_patterns()
        
        # Performance insights
        if perf.get('avg_execution_time', 0) > 3.0:
            insights['warnings'].append("⚠️ Average query time is slow. Consider indexing more files or upgrading hardware.")
        
        if perf.get('success_rate', 1.0) < 0.9:
            insights['warnings'].append("⚠️ Success rate below 90%. Check error logs for issues.")
        
        # Usage insights
        if patterns['file_searches'] > len(self.queries) * 0.7:
            insights['recommendations'].append("💡 You frequently search files. Consider organizing them better.")
        
        if self._get_top_items('tool_', 1):
            most_used = self._get_top_items('tool_', 1)[0]
            insights['recommendations'].append(f"💡 Most used tool: {most_used}. Create a shortcut for this.")
        
        # Error insights
        if len(self.error_log) > 0:
            most_common_error = self._get_most_common_errors(1)
            if most_common_error:
                insights['warnings'].append(f"⚠️ Common error: {most_common_error[0]}")
        
        return insights
    
    def export_analytics(self, filepath: str = 'analytics.json') -> bool:
        """Export analytics to file"""
        
        try:
            data = {
                'session_report': self.get_session_report(),
                'insights': self.get_insights(),
                'trending_queries': self.get_trending_queries(10),
                'slow_queries': self.get_slow_queries(2.0, 10),
                'all_queries': self.queries,
                'errors': self.error_log,
                'export_time': datetime.now().isoformat()
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            logger.info(f"Analytics exported to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Export failed: {e}")
            return False
    
    def generate_html_report(self, filepath: str = 'report.html') -> bool:
        """Generate HTML report"""
        
        try:
            perf = self.get_performance_summary()
            patterns = self.get_usage_patterns()
            insights = self.get_insights()
            session = self.get_session_report()
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Jonty Analytics Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    h1 {{ color: #1f77b4; }}
                    .metric {{ background: #f0f2f6; padding: 10px; margin: 10px 0; border-radius: 5px; }}
                    .warning {{ color: #d62728; }}
                    .recommendation {{ color: #2ca02c; }}
                    table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
                    th {{ background-color: #1f77b4; color: white; }}
                </style>
            </head>
            <body>
                <h1>Jonty Analytics Report</h1>
                
                <h2>Session Overview</h2>
                <div class="metric">
                    <p><strong>Duration:</strong> {session['session_duration_formatted']}</p>
                    <p><strong>Total Queries:</strong> {session['total_queries']}</p>
                    <p><strong>Total Errors:</strong> {session['total_errors']}</p>
                </div>
                
                <h2>Performance Metrics</h2>
                <div class="metric">
                    <p><strong>Average Execution Time:</strong> {perf.get('avg_execution_time', 0):.2f}s</p>
                    <p><strong>Median Execution Time:</strong> {perf.get('median_execution_time', 0):.2f}s</p>
                    <p><strong>Success Rate:</strong> {perf.get('success_rate', 0):.0%}</p>
                </div>
                
                <h2>Usage Patterns</h2>
                <div class="metric">
                    <p><strong>File Searches:</strong> {patterns['file_searches']}</p>
                    <p><strong>Most Used Tools:</strong> {', '.join(patterns['most_used_tools']) if patterns['most_used_tools'] else 'N/A'}</p>
                </div>
                
                <h2>Insights</h2>
                {''.join([f'<p class="warning">⚠️ {w}</p>' for w in insights['warnings']])}
                {''.join([f'<p class="recommendation">💡 {r}</p>' for r in insights['recommendations']])}
                
            </body>
            </html>
            """
            
            with open(filepath, 'w') as f:
                f.write(html)
            
            logger.info(f"HTML report generated: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return False
    
    def _get_top_items(self, prefix: str, n: int) -> List[str]:
        """Get top N items by prefix"""
        
        items = [(k.replace(prefix, ''), v) for k, v in self.user_patterns.items() if k.startswith(prefix)]
        items.sort(key=lambda x: x[1], reverse=True)
        return [item[0] for item in items[:n]]
    
    def _categorize_queries(self) -> Dict[str, int]:
        """Categorize queries by type"""
        
        categories = defaultdict(int)
        
        for q in self.queries:
            query_lower = q['query'].lower()
            
            if any(w in query_lower for w in ['search', 'find', 'look']):
                categories['search'] += 1
            elif any(w in query_lower for w in ['calculate', 'compute', '+', '-', '*', '/']):
                categories['calculation'] += 1
            elif any(w in query_lower for w in ['open', 'file', 'launch']):
                categories['file_operation'] += 1
            else:
                categories['general'] += 1
        
        return dict(categories)
    
    def _get_most_common_errors(self, n: int = 5) -> List[str]:
        """Get most common errors"""
        
        from collections import Counter
        
        errors = [e['error'] for e in self.error_log]
        most_common = Counter(errors).most_common(n)
        
        return [error[0] for error in most_common]
