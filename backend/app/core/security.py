"""
Minimal API-key auth for write operations (POST/PATCH/DELETE).

Set API_KEY in .env; write requests must send it in the `X-API-Key` header.
Read (GET) endpoints stay public.

Upgrade path: replace with real user accounts + JWT once you have roles
(coordinator / field volunteer / admin).
"""

import os
from fastapi import Header, HTTPException
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "change-me-in-env")


def require_api_key(x_api_key: str = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key (X-API-Key header)")
    return True
