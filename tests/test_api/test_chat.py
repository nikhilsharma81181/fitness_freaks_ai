"""Test the chat endpoint."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_chat_endpoint(client, mock_llm_response, mock_intent_classifier):
    """Test that the chat endpoint returns a 200 status code and the correct structure."""
    # Mock the async function
    mock_llm_response.side_effect = AsyncMock(return_value="This is a mock response from the LLM.")
    mock_intent_classifier.side_effect = AsyncMock(return_value=("workout_planning", 0.95))
    
    # Test data
    test_data = {
        "messages": [
            {"role": "user", "content": "I want to start working out."}
        ],
        "user_id": "test_user"
    }
    
    # Make request
    response = client.post("/api/v1/chat", json=test_data)
    
    # Check response
    assert response.status_code == 200
    assert "response" in response.json()
    assert "intent" in response.json()
    assert response.json()["intent"]["category"] == "workout_planning"
    assert response.json()["intent"]["confidence"] == 0.95
    assert "extracted_data" in response.json()
    assert "suggested_actions" in response.json()

@pytest.mark.asyncio
async def test_chat_endpoint_empty_messages(client):
    """Test that the chat endpoint returns a 400 when no messages are provided."""
    # Test data with empty messages
    test_data = {
        "messages": [],
        "user_id": "test_user"
    }
    
    # Make request
    response = client.post("/api/v1/chat", json=test_data)
    
    # Check response
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "No messages provided" in response.json()["detail"]

@pytest.mark.asyncio
async def test_chat_endpoint_no_user_message(client):
    """Test that the chat endpoint returns a 400 when no user message is found."""
    # Test data with only assistant messages
    test_data = {
        "messages": [
            {"role": "assistant", "content": "How can I help you?"}
        ],
        "user_id": "test_user"
    }
    
    # Make request
    response = client.post("/api/v1/chat", json=test_data)
    
    # Check response
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "No user message found" in response.json()["detail"]