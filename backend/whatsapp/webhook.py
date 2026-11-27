import hmac
import logging

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel

from backend.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["webhook"])


class AdapterEvent(BaseModel):
    """A temporary event shape for Day 6. Day 10 replaces it with the
    full normalized message structure."""

    event_type: str
    chat_id: str
    is_group: bool = False
    provider_message_id: str | None = None
    sender_id: str | None = None
    text: str | None = None


def mask_id(value: str | None) -> str:
    """Hide a WhatsApp ID or phone number so only the last 4 digits remain."""
    if not value:
        return "unknown"
    return "***" + value.split("@")[0][-4:]


def verify_adapter_secret(x_adapter_secret: str | None = Header(default=None)) -> None:
    """Deny by default: only the Node adapter, which knows the shared secret,
    may call the webhook."""
    expected = settings.adapter_shared_secret.get_secret_value()
    if not expected:
        raise HTTPException(status_code=503, detail="Adapter secret is not configured")
    if x_adapter_secret is None or not hmac.compare_digest(
        x_adapter_secret.encode(), expected.encode()
    ):
        raise HTTPException(status_code=401, detail="Invalid adapter secret")


@router.post("/adapter/event", dependencies=[Depends(verify_adapter_secret)])
def receive_adapter_event(event: AdapterEvent):
    # Log metadata only: never the full message text or the full phone number.
    logger.info(
        "adapter event: type=%s group=%s chat=%s sender=%s has_text=%s",
        event.event_type,
        event.is_group,
        mask_id(event.chat_id),
        mask_id(event.sender_id),
        bool(event.text),
    )
    return {"status": "received"}