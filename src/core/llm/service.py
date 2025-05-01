import os
import logging
import time
from typing import Dict, Any, List, Optional
import yaml
from dotenv import load_dotenv

# Langchain imports
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class LLMService:
    """Service for interacting with Language Model providers."""
    
    def __init__(self):
        """Initialize LLM service with config."""
        self.config = self._load_config()
        self.provider = os.getenv("LLM_PROVIDER", self.config.get("llm", {}).get("default_provider", "gemini"))
        self.models = {}
        self._initialize_models()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from config.yaml"""
        try:
            with open("config.yaml", "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {}
    
    def _initialize_models(self):
        """Initialize LLM models based on configuration."""
        llm_config = self.config.get("llm", {})
        
        # Initialize Google Gemini
        if "gemini" in llm_config.get("providers", {}):
            gemini_config = llm_config["providers"]["gemini"]
            try:
                google_api_key = os.getenv("GOOGLE_API_KEY")
                if google_api_key:
                    self.models["gemini"] = ChatGoogleGenerativeAI(
                        model=os.getenv("GEMINI_MODEL", gemini_config.get("default_model")),
                        temperature=gemini_config.get("temperature", 0.7),
                        max_output_tokens=gemini_config.get("max_tokens", 2000),
                        google_api_key=google_api_key,
                    )
                    logger.info("Google Gemini model initialized successfully")
                else:
                    logger.warning("GOOGLE_API_KEY not found. Google Gemini initialization skipped.")
            except Exception as e:
                logger.error(f"Error initializing Google Gemini model: {e}")
        
        # Initialize Groq
        if "groq" in llm_config.get("providers", {}):
            groq_config = llm_config["providers"]["groq"]
            try:
                groq_api_key = os.getenv("GROQ_API_KEY")
                if groq_api_key:
                    self.models["groq"] = ChatGroq(
                        model_name=os.getenv("GROQ_MODEL", groq_config.get("default_model")),
                        temperature=groq_config.get("temperature", 0.7),
                        max_tokens=groq_config.get("max_tokens", 2000),
                        groq_api_key=groq_api_key,
                    )
                    logger.info("Groq model initialized successfully")
                else:
                    logger.warning("GROQ_API_KEY not found. Groq initialization skipped.")
            except Exception as e:
                logger.error(f"Error initializing Groq model: {e}")
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        provider: Optional[str] = None,
        retry_count: int = 3,
        retry_delay: int = 2
    ) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            provider: Optional provider override (gemini or groq)
            retry_count: Number of retries on failure
            retry_delay: Delay between retries in seconds
            
        Returns:
            The LLM's response text
        """
        active_provider = provider or self.provider
        
        if active_provider not in self.models:
            logger.error(f"Provider {active_provider} not initialized")
            raise ValueError(f"Provider {active_provider} not available")
        
        langchain_messages = []
        
        # Gemini requires special handling for system prompts
        if active_provider == "gemini":
            # For Gemini, we prepend the system message to the first user message
            system_content = ""
            user_messages = []
            assistant_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_content += msg["content"] + "\n\n"
                elif msg["role"] == "user":
                    user_messages.append(msg["content"])
                elif msg["role"] == "assistant":
                    assistant_messages.append(msg["content"])
            
            # First alternating message must be from user
            if user_messages:
                # Prepend system prompt to first user message if there's a system prompt
                if system_content:
                    first_user_msg = f"[System Instructions]\n{system_content}\n\n[User Message]\n{user_messages[0]}"
                else:
                    first_user_msg = user_messages[0]
                
                langchain_messages.append(HumanMessage(content=first_user_msg))
                
                # Add the rest of the messages in alternating order
                for i in range(len(assistant_messages)):
                    langchain_messages.append(AIMessage(content=assistant_messages[i]))
                    if i + 1 < len(user_messages):
                        langchain_messages.append(HumanMessage(content=user_messages[i + 1]))
            else:
                # Fallback if no user messages
                langchain_messages.append(HumanMessage(content=system_content))
        else:
            # Standard handling for other providers
            for msg in messages:
                if msg["role"] == "system":
                    langchain_messages.append(SystemMessage(content=msg["content"]))
                elif msg["role"] == "user":
                    langchain_messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    langchain_messages.append(AIMessage(content=msg["content"]))
        
        for attempt in range(retry_count):
            try:
                response = await self.models[active_provider].agenerate([langchain_messages])
                return response.generations[0][0].text
            except Exception as e:
                logger.error(f"Error generating response (attempt {attempt+1}/{retry_count}): {e}")
                if attempt < retry_count - 1:
                    time.sleep(retry_delay)
                else:
                    raise
    
    def get_prompt_template(self, template_name: str) -> str:
        """Get a prompt template from the configuration."""
        return self.config.get("prompts", {}).get(template_name, "")


# Singleton instance
_instance = None

def get_llm_service() -> LLMService:
    """Get the LLM service singleton instance."""
    global _instance
    if _instance is None:
        _instance = LLMService()
    return _instance


