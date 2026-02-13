"""
Basic tests for the YOLO26 Object Detection API.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code in [200, 404]  # 404 if demo.html not found


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/v1/detection/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data


def test_docs_endpoint():
    """Test API documentation endpoint."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_detection_endpoint_without_file():
    """Test detection endpoint without file (should fail)."""
    response = client.post("/api/v1/detection/detect")
    assert response.status_code == 422  # Validation error


def test_detection_image_endpoint_without_file():
    """Test detection image endpoint without file (should fail)."""
    response = client.post("/api/v1/detection/detect/image")
    assert response.status_code == 422  # Validation error

