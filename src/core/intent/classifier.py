import logging
import yaml
from typing import Dict, Any, List, Tuple, Optional
import os
import json

# Import LLM service
from src.core.llm.service import get_llm_service

logger = logging.getLogger(__name__)

class IntentClassifier:
    """Classifier for determining user intent from natural language messages."""
    
    def __init__(self):
        """Initialize the intent classifier with configuration."""
        self.config = self._load_config()
        self.categories = self.config.get("intent", {}).get("categories", [
            "workout_planning",
            "workout_logging",
            "diet_planning",
            "diet_logging",
            "progress_tracking",
            "workout_session_management",
            "general_fitness_advice"
        ])
        self.threshold = self.config.get("intent", {}).get("threshold", 0.7)
        self.llm_service = get_llm_service()
        
        logger.info(f"Intent classifier initialized with {len(self.categories)} categories")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from config.yaml"""
        try:
            with open("config.yaml", "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {}
    
    async def classify(self, message: str) -> Tuple[str, float]:
        """
        Classify the user's message to determine intent.
        
        Args:
            message: The user's message
            
        Returns:
            A tuple of (intent_category, confidence_score)
        """
        # Create a prompt for the LLM to classify the intent
        system_prompt = f"""You are an intent classifier for a fitness coaching application.
You need to classify the user's message into one of the following categories:
{', '.join(self.categories)}

You should respond ONLY with a JSON object in this format:
{{
    "category": "the_intent_category",
    "confidence": 0.0 to 1.0,
    "reasoning": "Brief explanation of why you chose this category"
}}

DO NOT include any other text in your response. Only the JSON object.
"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        try:
            response = await self.llm_service.generate_response(messages)
            
            # Extract JSON from response
            try:
                # In case the model returns additional text around the JSON
                # We try to find and parse just the JSON part
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx]
                    result = json.loads(json_str)
                    
                    category = result.get("category", "general_fitness_advice")
                    confidence = result.get("confidence", 0.0)
                    
                    # Validate the category
                    if category not in self.categories:
                        logger.warning(f"LLM returned invalid category: {category}, defaulting to general_fitness_advice")
                        category = "general_fitness_advice"
                        confidence = 0.5
                    
                    # If confidence is below threshold, default to general advice
                    if confidence < self.threshold:
                        logger.info(f"Low confidence ({confidence}) for {category}, defaulting to general_fitness_advice")
                        if category != "general_fitness_advice":
                            category = "general_fitness_advice"
                            confidence = max(confidence, 0.5)  # Set a minimum confidence
                    
                    return category, confidence
                else:
                    logger.error(f"Could not extract JSON from LLM response: {response}")
                    return "general_fitness_advice", 0.5
                    
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing JSON from LLM response: {e}")
                logger.debug(f"Problematic response: {response}")
                return "general_fitness_advice", 0.5
                
        except Exception as e:
            logger.error(f"Error classifying intent: {e}")
            return "general_fitness_advice", 0.5
    
    async def get_fallback_response(self, message: str) -> str:
        """
        Generate a fallback response when intent classification fails.
        
        Args:
            message: The user's message
            
        Returns:
            A general fitness advice response
        """
        system_prompt = """You are a helpful fitness assistant. 
The user's request could not be classified into a specific category.
Provide a helpful, general response about fitness. If appropriate, 
ask clarifying questions to better understand what they need."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        try:
            return await self.llm_service.generate_response(messages)
        except Exception as e:
            logger.error(f"Error generating fallback response: {e}")
            return "I'm sorry, I'm having trouble understanding your request. Could you please rephrase it or provide more details about what you need help with regarding your fitness journey?"


# Singleton instance
_instance = None

def get_intent_classifier() -> IntentClassifier:
    """Get the intent classifier singleton instance."""
    global _instance
    if _instance is None:
        _instance = IntentClassifier()
    return _instance