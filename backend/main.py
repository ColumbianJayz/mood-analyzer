from fastapi import FastAPI
from spotify import get_token 
import httpx

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/search")
async def search(q: str):
    token = await get_token()
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.spotify.com/v1/search",
            params={"q": q, "type": "track"},
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        data = response.json()
        tracks = data["tracks"]["items"]

        results = []
        for track in tracks: 
            results.append({
                "name": track["name"], 
                "artist": track["artists"][0]["name"],
                "album_art": track["album"]["images"][0]["url"],
                "spotify_id": track["id"]
            })
        return results


