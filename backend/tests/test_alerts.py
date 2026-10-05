from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_create_alert():
    alert_data = {
        "rule_id": "RULE-001",
        "rule_name": "Test Rule",
        "source": "192.168.1.100",
        "severity": "HIGH",
        "evidence": "{}",
        "analyst_action": "Investigate"
    }
    response = client.post("/api/alerts/", json=alert_data)
    assert response.status_code == 200
    data = response.json()
    assert data["rule_id"] == "RULE-001"
    assert "alert_id" in data
