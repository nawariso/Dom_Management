import hmac
import os
from hashlib import sha256

from fastapi import HTTPException, Request, status

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "webhook-secret")


async def verify_signature(request: Request, header_name: str = "X-Signature") -> None:
    provided_signature = request.headers.get(header_name)
    if not provided_signature:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing signature")

    body = await request.body()
    computed_signature = hmac.new(WEBHOOK_SECRET.encode(), body, sha256).hexdigest()

    if not hmac.compare_digest(provided_signature, computed_signature):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid webhook signature")
