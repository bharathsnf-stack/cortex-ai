"""
Cortex AI - Core Brain Module
Handles reasoning, decision making, and response generation
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class CortexBrain:
    """
    Main brain of Cortex AI system
    Processes inputs and generates intelligent responses
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.memory = []
        self.context = {}
        self.plugins = {}
        logger.info("Cortex Brain initialized")
    
    async def process_input(self, user_input: str) -> Dict:
        """
        Process user input and generate response
        
        Args:
            user_input: Text input from user
            
        Returns:
            Dict containing response and metadata
        """
        logger.info(f"Processing input: {user_input[:50]}...")
        
        # Store in short-term memory
        self._store_memory(user_input, "input")
        
        # Analyze intent
        intent = self._analyze_intent(user_input)
        
        # Generate response
        response = await self._generate_response(user_input, intent)
        
        # Store response in memory
        self._store_memory(response, "output")
        
        return {
            "response": response,
            "intent": intent,
            "timestamp": datetime.now().isoformat(),
            "confidence": 0.85
        }
    
    def _analyze_intent(self, text: str) -> str:
        """Analyze user intent from input"""
        # Simple keyword-based intent (extend with ML models)
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["hello", "hi", "hey"]):
            return "greeting"
        elif any(word in text_lower for word in ["help", "assist", "support"]):
            return "help_request"
        elif "?" in text:
            return "question"
        else:
            return "statement"
    
    async def _generate_response(self, input_text: str, intent: str) -> str:
        """Generate appropriate response based on intent"""
        
        responses = {
            "greeting": "Hello! I'm Cortex AI. How can I assist you today?",
            "help_request": "I'm here to help! What do you need assistance with?",
            "question": f"That's an interesting question. Let me think about: {input_text}",
            "statement": "I understand. Please tell me more."
        }
        
        return responses.get(intent, "I'm processing your request...")
    
    def _store_memory(self, content: str, memory_type: str):
        """Store interaction in memory"""
        self.memory.append({
            "content": content,
            "type": memory_type,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 100 interactions
        if len(self.memory) > 100:
            self.memory = self.memory[-100:]
    
    def get_memory(self, limit: int = 10) -> List[Dict]:
        """Retrieve recent memory"""
        return self.memory[-limit:]
    
    def clear_memory(self):
        """Clear all memory"""
        self.memory = []
        logger.info("Memory cleared")
