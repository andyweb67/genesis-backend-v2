# /dependencies/security.py

from fastapi import Header, HTTPException, status
from core.config import settings

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.GENESIS_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API Key."
        )
