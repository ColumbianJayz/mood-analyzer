from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/search")
async def search(q: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.deezer.com/search",
            params={"q": q},
        )
        response.raise_for_status()
        data = response.json()
        tracks = data["data"]

        results = []
        for track in tracks: 
            results.append({
                "title": track["title"], 
                "artist": track["artist"]["name"],
                "album_art": track["album"]["cover_medium"],
                "deezer_id": track["id"],
                "preview": track["preview"]
            })
        return results


