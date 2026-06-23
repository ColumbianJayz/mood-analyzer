import os
import time
import httpx
from dotenv import load_dotenv

load_dotenv()
_token = None 
_token_expires_at = 0

async def get_token() -> str:
    global _token, _token_expires_at
    if _token and time.time() < _token_expires_at:
        return _token
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://accounts.spotify.com/api/token", 
            data={"grant_type": "client_credentials"},
            auth=(os.getenv("SPOTIFY_CLIENT_ID"), os.getenv("SPOTIFY_CLIENT_SECRET"))
        )
        response.raise_for_status()
        data = response.json()
        _token = data["access_token"]
        _token_expires_at = time.time() + data["expires_in"] - 30
        return _token
    
