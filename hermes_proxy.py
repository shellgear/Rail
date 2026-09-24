"""
Hermes Proxy Server - HTTP endpoint for Rail avatar to communicate with Hermes.

This server provides a simple HTTP API that Rail can use to send messages to Hermes
and receive responses, with Bearer token authentication.

Usage:
    python hermes_proxy.py

Environment variables:
    HERMES_PROXY_TOKEN - The Bearer token for authentication (required)
    HERMES_WEBHOOK_URL - The webhook URL to send requests to (default: http://localhost:8644/webhooks/rail-proxy)
    HERMES_WEBHOOK_SECRET - The webhook secret for HMAC validation (optional)
"""

import os
import json
import hashlib
import hmac
import httpx
from fastapi import FastAPI, HTTPException, Header, Request
from pydantic import BaseModel
from typing import Optional

# Configuration
PROXY_TOKEN = os.getenv("HERMES_PROXY_TOKEN")
WEBHOOK_URL = os.getenv("HERMES_WEBHOOK_URL", "http://localhost:8644/webhooks/rail-proxy")
WEBHOOK_SECRET = os.getenv("HERMES_WEBHOOK_SECRET", "")

if not PROXY_TOKEN:
    raise ValueError("HERMES_PROXY_TOKEN environment variable is required")

app = FastAPI(
    title="Hermes Proxy",
    description="HTTP proxy for Rail avatar to communicate with Hermes Agent",
    version="1.0.0"
)


class MessageRequest(BaseModel):
    """Request body for sending a message to Hermes."""
    message: str
    user_id: Optional[str] = None
    channel: Optional[str] = "rail"


class MessageResponse(BaseModel):
    """Response from Hermes."""
    success: bool
    response: Optional[str] = None
    error: Optional[str] = None
    request_id: Optional[str] = None


def validate_bearer_token(authorization: Optional[str]) -> bool:
    """Validate Bearer token from Authorization header."""
    if not authorization:
        return False
    if not authorization.startswith("Bearer "):
        return False
    token = authorization[7:]  # Remove "Bearer " prefix
    return token == PROXY_TOKEN


def create_hmac_signature(payload: str, secret: str) -> str:
    """Create HMAC-SHA256 signature for webhook payload."""
    if not secret:
        return ""
    return hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()


@app.post("/send", response_model=MessageResponse)
async def send_message(
    request: MessageRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Send a message to Hermes and get a response.
    
    Requires Bearer token authentication via Authorization header.
    Example:
        curl -X POST http://localhost:8000/send \\
             -H "Authorization: Bearer YOUR_TOKEN" \\
             -H "Content-Type: application/json" \\
             -d '{"message": "ciao", "user_id": "123"}'
    """
    # Validate authentication
    if not validate_bearer_token(authorization):
        raise HTTPException(status_code=401, detail="Invalid or missing authentication token")
    
    try:
        # Prepare payload for webhook
        payload = {
            "message": request.message,
            "user_id": request.user_id,
            "channel": request.channel
        }
        payload_json = json.dumps(payload)
        
        # Prepare headers for webhook
        headers = {
            "Content-Type": "application/json"
        }
        
        # Add HMAC signature if secret is configured
        if WEBHOOK_SECRET:
            signature = create_hmac_signature(payload_json, WEBHOOK_SECRET)
            headers["X-Webhook-Signature"] = f"sha256={signature}"
        
        # Send request to Hermes webhook
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                WEBHOOK_URL,
                json=payload,
                headers=headers
            )
        
        if response.status_code == 200:
            result = response.json()
            return MessageResponse(
                success=True,
                response=result.get("response", result.get("message", str(result))),
                request_id=result.get("id")
            )
        else:
            return MessageResponse(
                success=False,
                error=f"Webhook error: {response.status_code} - {response.text}"
            )
    
    except httpx.RequestError as e:
        return MessageResponse(
            success=False,
            error=f"Failed to connect to Hermes: {str(e)}"
        )
    except Exception as e:
        return MessageResponse(
            success=False,
            error=f"Internal error: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "hermes-proxy"}


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "Hermes Proxy",
        "version": "1.0.0",
        "endpoints": {
            "POST /send": "Send message to Hermes (requires Bearer token)",
            "GET /health": "Health check",
            "GET /": "API info"
        },
        "authentication": "Bearer token via Authorization header"
    }


if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Hermes Proxy Server")
    print(f"📡 Webhook URL: {WEBHOOK_URL}")
    print(f"🔐 Token configured: {'Yes' if PROXY_TOKEN else 'No'}")
    print()
    print("Start your Rail avatar to connect!")
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
