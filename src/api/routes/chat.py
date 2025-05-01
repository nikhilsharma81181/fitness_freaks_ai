import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Dict, Any

# Import services
from src.core.llm.service import get_llm_service
from src.core.intent.classifier import get_intent_classifier
from src.core.llm.prompts import get_prompt_for_intent

# Import schemas
from src.api.models.schemas import (
    Message, 
    ChatRequest, 
    ChatResponse, 
    IntentInfo,
    SuggestedAction
)

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    llm_service = Depends(get_llm_service),
    intent_classifier = Depends(get_intent_classifier)
):
    """
    Process a chat request from the user and generate a response.
    
    Args:
        request: The chat request containing message history
        
    Returns:
        The assistant's response and intent classification
    """
    try:
        # Extract the user's latest message
        if not request.messages or len(request.messages) == 0:
            raise HTTPException(status_code=400, detail="No messages provided")
        
        latest_user_message = None
        for message in reversed(request.messages):
            if message.role == "user":
                latest_user_message = message.content
                break
        
        if not latest_user_message:
            raise HTTPException(status_code=400, detail="No user message found")
        
        # Classify the user's intent
        intent, confidence = await intent_classifier.classify(latest_user_message)
        logger.info(f"Classified intent: {intent} (confidence: {confidence:.2f})")
        
        # Get the appropriate prompt template based on intent
        system_prompt = get_prompt_for_intent(intent)
        
        # Format messages for the LLM
        formatted_messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (limit to last 10 messages for context)
        for message in request.messages[-10:]:
            formatted_messages.append({
                "role": message.role,
                "content": message.content
            })
        
        # Generate response
        response_text = await llm_service.generate_response(formatted_messages)
        
        return ChatResponse(
            response=response_text,
            intent=IntentInfo(
                category=intent,
                confidence=confidence
            ),
            extracted_data={},  # In the future, we'll extract structured data here
            suggested_actions=[]  # In the future, we'll suggest actions based on intent
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")