from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_root_returns_welcome():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hi, I'm AK. Welcome to Study Mate!",
        "status": "Running",
        "project": "Study Mate",
        "agent": "AK",
    }


def test_health_returns_healthy():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "application": "Study Mate",
        "agent": "AK",
    }


def test_info_matches_config_types():
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert set(data) == {"app_name", "agent_name", "app_version", "debug"}
    assert data["app_name"] == "Study Mate"
    assert data["agent_name"] == "AK"
    assert isinstance(data["debug"], bool)


def test_echo_valid_message():
    response = client.post("/echo", json={"message": "Hello AK"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello AK", "length": 8, "agent": "AK"}


def test_echo_empty_message_rejected():
    response = client.post("/echo", json={"message": ""})
    assert response.status_code == 422


def test_echo_missing_message_rejected():
    response = client.post("/echo", json={})
    assert response.status_code == 422


def test_echo_too_long_message_rejected():
    response = client.post("/echo", json={"message": "a" * 501})
    assert response.status_code == 422