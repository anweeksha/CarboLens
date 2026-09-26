"""Tests for health check endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "CarbonLens API"


def test_get_database_health_unconfigured():
    # Without DATABASE_URL set/connected, endpoint returns HTTP 503
    response = client.get("/api/health/db")
    assert response.status_code in (200, 503)
    data = response.json()
    assert "status" in data
    assert "database" in data
