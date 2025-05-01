"""Pytest configuration for Fitness Coach AI tests."""

import pytest
import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from unittest.mock import patch

# Load environment variables from .env.test if it exists, otherwise from .env
if os.path.exists(".env.test"):
    load_dotenv(".env.test")
else:
    load_dotenv()

# Set environment to testing
os.environ["ENV"] = "testing"

# Mock LLM responses for testing
@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing."""
    with patch("src.core.llm.service.LLMService.generate_response") as mock:
        mock.return_value = "This is a mock response from the LLM."
        yield mock

@pytest.fixture
def mock_intent_classifier():
    """Mock intent classifier for testing."""
    with patch("src.core.intent.classifier.IntentClassifier.classify") as mock:
        mock.return_value = ("workout_planning", 0.95)
        yield mock

@pytest.fixture
def client():
    """Test client for the FastAPI app."""
    from src.main import app
    
    with TestClient(app) as client:
        yield client