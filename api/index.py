from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import json

app = FastAPI()

# Allow CORS biar bot lo bisa akses
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
        'extract_flat': not download,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    }

@app.get("/api/search")
async def search(q: str = Query(..., description="Query pencarian")):
    try:
        ydl_opts = get_ydl_opts(download=False)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Search YouTube
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
        # Pake yt-dlp buat dapet direct link audio (biasanya m4a/webm)
        # Ini gantiin fungsi convert karena link ini bisa langsung diputar/download
        ydl_opts = get_ydl_opts(download=True)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Cari format audio terbaik
            audio_url = info.get('url')
            title = info.get('title')
            
            return {
                "success": True,
                "title": title,
                "data": audio_url,  # Ini link direct ke server Google/YouTube
                "format": info.get('ext'),
                "thumbnail": info.get('thumbnail')
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mock route untuk convert (biar bot lo ga error pas manggil)
@app.get("/api/convert")
async def convert():
    return {"message": "Direct link provided in /download, no conversion needed on server side."}
