"""
Jonty Chat Agent - Advanced Conversation Management
Maintains context, understands intents, handles multi-turn dialogues
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import deque

logger = logging.getLogger(__name__)


class ChatAgent:
    """Advanced conversational agent with context management"""
    
    def __init__(self, base_agent):
        """Initialize Chat Agent"""
        self.base_agent = base_agent
        self.conversation_history = deque(maxlen=50)  # Keep last 50 messages
        self.context_window = deque(maxlen=10)  # Active context
        self.topics = []  # Track conversation topics
        self.user_preferences = {}
        
        logger.info("Chat Agent initialized")
    
    def chat(self, user_message: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process chat message with full context
        
        Args:
            user_message: User's message
            user_id: Optional user identifier
            
        Returns:
            Conversational response with context
        """
        
        logger.info(f"Chat message: {user_message}")
        
        # Step 1: Update context
        self.context_window.append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Step 2: Extract intent
        intent = self._extract_intent(user_message)
        
        # Step 3: Get response
        if intent['type'] == 'greeting':
            response = self._handle_greeting(user_message)
        elif intent['type'] == 'clarification':
            response = self._handle_clarification(user_message)
        elif intent['type'] == 'follow_up':
            response = self._handle_follow_up(user_message)
        else:
            response = self._handle_general(user_message)
        
        # Step 4: Add to history
        self.conversation_history.append({
            'user': user_message,
            'assistant': response['text'],
            'intent': intent['type'],
            'timestamp': datetime.now().isoformat()
        })
        
        # Step 5: Update topics
        self._update_topics(intent)
        
        return {
            'success': True,
            'response': response['text'],
            'intent': intent['type'],
            'context': {
                'current_topic': self.topics[-1] if self.topics else 'general',
                'conversation_turn': len(self.conversation_history),
                'context_used': response.get('context_used', False)
            },
            'suggested_follow_ups': self._suggest_follow_ups(user_message)
        }
    
    def _extract_intent(self, message: str) -> Dict[str, Any]:
        """Extract user intent from message"""
        
        message_lower = message.lower()
        
        # Greeting patterns
        if any(w in message_lower for w in ['hello', 'hi', 'hey', 'good morning', 'greetings']):
            return {'type': 'greeting', 'confidence': 0.95}
        
        # Clarification patterns
        if any(w in message_lower for w in ['what do you mean', 'explain', 'clarify', 'repeat']):
            return {'type': 'clarification', 'confidence': 0.90}
        
        # Follow-up patterns
        if any(w in message_lower for w in ['more', 'add', 'also', 'furthermore', 'plus']):
            return {'type': 'follow_up', 'confidence': 0.85}
        
        # Information request
        if any(w in message_lower for w in ['what', 'where', 'when', 'who', 'which', 'how']):
            return {'type': 'information_request', 'confidence': 0.80}
        
        # Command patterns
        if any(w in message_lower for w in ['do', 'execute', 'run', 'perform', 'open', 'search']):
            return {'type': 'command', 'confidence': 0.85}
        
        return {'type': 'general', 'confidence': 0.5}
    
    def _handle_greeting(self, message: str) -> Dict[str, str]:
        """Handle greeting messages"""
        
        greetings = [
            "Hey there! 👋 I'm Jonty, your personal AI assistant. How can I help you today?",
            "Hello! 😊 I'm here to help you search your files, answer questions, or perform tasks. What would you like to do?",
            "Hi! Welcome! 🚀 What can I assist you with?"
        ]
        
        import random
        return {'text': random.choice(greetings), 'context_used': False}
    
    def _handle_clarification(self, message: str) -> Dict[str, str]:
        """Handle clarification requests"""
        
        if len(self.conversation_history) < 2:
            response = "I don't have a previous response to clarify. Could you ask me something?"
        else:
            prev_response = self.conversation_history[-1]['assistant']
            response = f"Let me clarify my previous response:\n\n{prev_response}\n\nWould you like me to explain anything specific?"
        
        return {'text': response, 'context_used': True}
    
    def _handle_follow_up(self, message: str) -> Dict[str, str]:
        """Handle follow-up questions"""
        
        # Get context from previous exchange
        if len(self.conversation_history) < 1:
            response = self.base_agent.process_query(message)
            return {'text': response['response']}
        
        # Process with context
        context_msg = f"Previous context: {self.conversation_history[-1]['user']}\n\nFollow-up: {message}"
        response = self.base_agent.process_query(context_msg, search_files=True)
        
        return {'text': response['response'], 'context_used': True}
    
    def _handle_general(self, message: str) -> Dict[str, str]:
        """Handle general queries"""
        
        response = self.base_agent.process_query(message, search_files=True)
        return {'text': response['response']}
    
    def _update_topics(self, intent: Dict):
        """Update conversation topics"""
        
        intent_type = intent['type']
        if intent_type not in self.topics:
            self.topics.append(intent_type)
    
    def _suggest_follow_ups(self, message: str) -> List[str]:
        """Suggest possible follow-up questions"""
        
        suggestions = []
        
        if 'python' in message.lower():
            suggestions = [
                "Show me all Python files",
                "What Python libraries do I use?",
                "Search for Python tutorials"
            ]
        elif 'file' in message.lower() or 'search' in message.lower():
            suggestions = [
                "Find more files like this",
                "Show related documents",
                "Search in a specific folder"
            ]
        else:
            suggestions = [
                "Tell me more",
                "Can you explain further?",
                "Any suggestions?"
            ]
        
        return suggestions
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary of current conversation"""
        
        if not self.conversation_history:
            return {'summary': 'No conversation yet', 'turns': 0}
        
        summary = f"Conversation Summary:\n"
        summary += f"Total exchanges: {len(self.conversation_history)}\n"
        summary += f"Topics discussed: {', '.join(self.topics)}\n"
        summary += f"\nRecent messages:\n"
        
        for msg in list(self.conversation_history)[-5:]:
            summary += f"- User: {msg['user'][:50]}...\n"
        
        return {
            'summary': summary,
            'turns': len(self.conversation_history),
            'topics': self.topics
        }
    
    def set_user_preference(self, key: str, value: Any):
        """Set user preference"""
        
        self.user_preferences[key] = value
        logger.info(f"Preference set: {key} = {value}")
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """Get user preferences"""
        
        return self.user_preferences
    
    def reset_conversation(self):
        """Reset conversation history"""
        
        self.conversation_history.clear()
        self.context_window.clear()
        self.topics.clear()
        logger.info("Conversation reset")
    
    def export_conversation(self, filepath: str = 'conversation.json') -> bool:
        """Export conversation to file"""
        
        import json
        
        try:
            data = {
                'conversation': list(self.conversation_history),
                'topics': self.topics,
                'preferences': self.user_preferences,
                'export_time': datetime.now().isoformat()
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            logger.info(f"Conversation exported to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Export failed: {e}")
            return False
