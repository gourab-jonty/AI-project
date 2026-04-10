"""
Jonty Integration Agent - External API & Service Integration
Connect to web APIs, weather, calendar, email, etc.
"""

import logging
import json
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from datetime import datetime

logger = logging.getLogger(__name__)


class ServiceConnector(ABC):
    """Base class for service connectors"""
    
    @abstractmethod
    def connect(self) -> bool:
        """Connect to service"""
        pass
    
    @abstractmethod
    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute action on service"""
        pass


class WeatherService(ServiceConnector):
    """Weather service connector"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.connected = False
    
    def connect(self) -> bool:
        """Connect to weather service"""
        # In real implementation, validate API key
        self.connected = bool(self.api_key)
        return self.connected
    
    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute weather action"""
        
        if action == 'get_weather':
            location = kwargs.get('location', 'current')
            return {
                'status': 'success',
                'location': location,
                'temperature': 72,  # Mock data
                'condition': 'Sunny'
            }
        return {'status': 'error', 'message': 'Unknown action'}


class CalendarService(ServiceConnector):
    """Calendar service connector"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.connected = False
        self.events = []
    
    def connect(self) -> bool:
        """Connect to calendar service"""
        self.connected = bool(self.api_key)
        return self.connected
    
    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute calendar action"""
        
        if action == 'get_events':
            date = kwargs.get('date', datetime.now().date())
            return {
                'status': 'success',
                'date': str(date),
                'events': [
                    {'title': 'Meeting', 'time': '10:00 AM'},
                    {'title': 'Lunch', 'time': '12:00 PM'}
                ]
            }
        
        elif action == 'add_event':
            title = kwargs.get('title', 'Event')
            time = kwargs.get('time', '12:00 PM')
            self.events.append({'title': title, 'time': time})
            return {'status': 'success', 'message': f'Event "{title}" added'}
        
        return {'status': 'error', 'message': 'Unknown action'}


class EmailService(ServiceConnector):
    """Email service connector"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.connected = False
    
    def connect(self) -> bool:
        """Connect to email service"""
        self.connected = bool(self.api_key)
        return self.connected
    
    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute email action"""
        
        if action == 'send_email':
            to = kwargs.get('to', '')
            subject = kwargs.get('subject', '')
            body = kwargs.get('body', '')
            return {
                'status': 'success',
                'message': f'Email sent to {to}',
                'timestamp': datetime.now().isoformat()
            }
        
        elif action == 'check_inbox':
            return {
                'status': 'success',
                'unread_count': 3,
                'recent_emails': [
                    {'from': 'user@example.com', 'subject': 'Meeting tomorrow'},
                    {'from': 'boss@company.com', 'subject': 'Project update'}
                ]
            }
        
        return {'status': 'error', 'message': 'Unknown action'}


class WebSearchService(ServiceConnector):
    """Web search service connector"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.connected = False
    
    def connect(self) -> bool:
        """Connect to search service"""
        self.connected = bool(self.api_key)
        return self.connected
    
    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute search action"""
        
        if action == 'search':
            query = kwargs.get('query', '')
            return {
                'status': 'success',
                'query': query,
                'results': [
                    {'title': f'Result for {query}', 'url': 'https://example.com'},
                    {'title': f'More about {query}', 'url': 'https://example2.com'}
                ]
            }
        
        return {'status': 'error', 'message': 'Unknown action'}


class IntegrationAgent:
    """Main integration agent managing all external services"""
    
    def __init__(self):
        self.services: Dict[str, ServiceConnector] = {}
        self.integration_log = []
        self.config = {}
        
        logger.info("Integration Agent initialized")
    
    def register_service(self, name: str, service: ServiceConnector) -> bool:
        """Register external service"""
        
        if service.connect():
            self.services[name] = service
            logger.info(f"Service registered: {name}")
            return True
        else:
            logger.error(f"Failed to register service: {name}")
            return False
    
    def execute_integration(self, service_name: str, action: str, **kwargs) -> Dict[str, Any]:
        """Execute external service action"""
        
        if service_name not in self.services:
            return {
                'status': 'error',
                'message': f'Service not found: {service_name}',
                'available': list(self.services.keys())
            }
        
        try:
            result = self.services[service_name].execute(action, **kwargs)
            
            # Log integration
            self.integration_log.append({
                'service': service_name,
                'action': action,
                'status': result.get('status'),
                'timestamp': datetime.now().isoformat()
            })
            
            logger.info(f"Integration executed: {service_name}.{action}")
            return result
        except Exception as e:
            logger.error(f"Integration error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def execute_workflow(self, workflow: List[Dict]) -> List[Dict]:
        """Execute multi-step integration workflow"""
        
        results = []
        
        for step in workflow:
            service = step.get('service')
            action = step.get('action')
            params = step.get('params', {})
            
            result = self.execute_integration(service, action, **params)
            results.append(result)
        
        return results
    
    def get_available_services(self) -> List[str]:
        """List available services"""
        
        return list(self.services.keys())
    
    def get_integration_log(self) -> List[Dict]:
        """Get integration execution log"""
        
        return self.integration_log
    
    def setup_default_services(self) -> Dict[str, bool]:
        """Setup common services"""
        
        results = {}
        
        # These will be mock services - replace with real API keys in production
        results['weather'] = self.register_service('weather', WeatherService(api_key='mock'))
        results['calendar'] = self.register_service('calendar', CalendarService(api_key='mock'))
        results['email'] = self.register_service('email', EmailService(api_key='mock'))
        results['search'] = self.register_service('search', WebSearchService(api_key='mock'))
        
        return results
    
    def create_workflow_for_query(self, query: str) -> Optional[List[Dict]]:
        """Create integration workflow based on query"""
        
        query_lower = query.lower()
        workflow = []
        
        # Detect needed services
        if any(w in query_lower for w in ['weather', 'rain', 'temperature', 'forecast']):
            workflow.append({
                'service': 'weather',
                'action': 'get_weather',
                'params': {'location': 'current'}
            })
        
        if any(w in query_lower for w in ['calendar', 'meeting', 'appointment', 'schedule']):
            workflow.append({
                'service': 'calendar',
                'action': 'get_events',
                'params': {}
            })
        
        if any(w in query_lower for w in ['email', 'mail', 'inbox']):
            workflow.append({
                'service': 'email',
                'action': 'check_inbox',
                'params': {}
            })
        
        if any(w in query_lower for w in ['search', 'find on web', 'google']):
            search_query = query_lower.replace('search', '').replace('for', '').strip()
            workflow.append({
                'service': 'search',
                'action': 'search',
                'params': {'query': search_query}
            })
        
        return workflow if workflow else None
    
    def process_integrated_query(self, query: str) -> Dict[str, Any]:
        """Process query and execute integrations if needed"""
        
        workflow = self.create_workflow_for_query(query)
        
        if not workflow:
            return {
                'status': 'no_integration',
                'message': 'No external services needed for this query'
            }
        
        results = self.execute_workflow(workflow)
        
        return {
            'status': 'success',
            'workflow_steps': len(workflow),
            'results': results,
            'query': query
        }
    
    def export_integration_config(self, filepath: str = 'integrations.json'):
        """Export integration configuration"""
        
        config = {
            'services': list(self.services.keys()),
            'log': self.integration_log,
            'export_time': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2, default=str)
        
        logger.info(f"Integration config exported to {filepath}")
