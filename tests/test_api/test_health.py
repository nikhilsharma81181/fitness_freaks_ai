"""Test the health check endpoint."""

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test that the health endpoint returns a 200 status code and the correct structure."""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "ok"
    assert "version" in response.json()
    assert "environment" in response.json()
    assert "llm_provider" in response.json()

def test_root_endpoint():
    """Test that the root endpoint returns a 200 status code and the correct structure."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "docs" in response.json()
    assert "health" in response.json()