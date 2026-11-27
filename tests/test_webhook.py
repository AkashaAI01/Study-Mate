from fastapi.testclient import TestClient
from pydantic import SecretStr

from backend.config import settings
from backend.main import app

client = TestClient(app)

SECRET = "test-secret"
VALID_EVENT = {
    "event_type": "message",
    "chat_id": "120363000000000000@g.us",
    "is_group": True,
    "provider_message_id": "ABC123",
    "sender_id": "923001234567@s.whatsapp.net",
    "text": "hello AK",
}


def set_secret(monkeypatch, value=SECRET):
    monkeypatch.setattr(settings, "adapter_shared_secret", SecretStr(value))


def test_valid_secret_is_accepted(monkeypatch):
    set_secret(monkeypatch)
    response = client.post(
        "/webhook/adapter/event", json=VALID_EVENT, headers={"X-Adapter-Secret": SECRET}
    )
    assert response.status_code == 200
    assert response.json() == {"status": "received"}


def test_missing_secret_is_rejected(monkeypatch):
    set_secret(monkeypatch)
    response = client.post("/webhook/adapter/event", json=VALID_EVENT)
    assert response.status_code == 401


def test_wrong_secret_is_rejected(monkeypatch):
    set_secret(monkeypatch)
    response = client.post(
        "/webhook/adapter/event", json=VALID_EVENT, headers={"X-Adapter-Secret": "nope"}
    )
    assert response.status_code == 401


def test_unconfigured_secret_denies_everything(monkeypatch):
    set_secret(monkeypatch, "")
    response = client.post(
        "/webhook/adapter/event", json=VALID_EVENT, headers={"X-Adapter-Secret": ""}
    )
    assert response.status_code == 503


def test_auth_is_checked_before_body_validation(monkeypatch):
    set_secret(monkeypatch)
    response = client.post("/webhook/adapter/event", json={"junk": 1})
    assert response.status_code == 401


def test_bad_body_with_valid_secret_is_422(monkeypatch):
    set_secret(monkeypatch)
    response = client.post(
        "/webhook/adapter/event", json={"junk": 1}, headers={"X-Adapter-Secret": SECRET}
    )
    assert response.status_code == 422