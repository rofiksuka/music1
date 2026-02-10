from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_ydl_opts(download=False):
    return {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True, # Bypass SSL
        'geo_bypass': True,        # Bypass regional block
        'extract_flat': not download,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }

@app.get("/api/search")
async def search(q: str = Query(..., description="Query pencarian")):
    try:
        ydl_opts = get_ydl_opts(download=False)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch10:{q}", download=False)
            results = []
            for entry in info['entries']:
                results.append({
                    "id": entry.get("id"),
                    "title": entry.get("title"),
                    "url": f"https://www.youtube.com/watch?v={entry.get('id')}",
                    "duration": entry.get("duration"),
                    "thumbnail": entry.get("thumbnails")[0].get("url") if entry.get("thumbnails") else None,
                    "channel": entry.get("uploader"),
                })
            return {"query": q, "results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download")
async def download(url: str = Query(..., description="URL YouTube")):
    try:
        ydl_opts = get_ydl_opts(download=True)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # PENTING: extract_info bakal ngambil direct link yang fresh
            info = ydl.extract_info(url, download=False)
            audio_url = info.get('url')
            
            if not audio_url:
                raise Exception("Gagal dapet direct link")
                
            return {
                "success": True,
                "title": info.get('title'),
                "data": audio_url,
                "format": info.get('ext', 'm4a'),
                "thumbnail": info.get('thumbnail')
            }
    except Exception as e:
        # Kirim error detail ke bot biar lo tau kenapa gagal
        raise HTTPException(status_code=500, detail=f"YouTube Block: {str(e)}")
