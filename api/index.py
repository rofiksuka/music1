from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cookie sakti yang lo dapet tadi
MY_COOKIE = "__Secure-YNID=15.YT=evkBfi16pVF3S-F580Gc5k3Vxn2Z1ToL-v-Taqlu3o8uSKGVJL45O6lydZU9uyrB3r5M1FHgU8r68vqAN6uan7WkE9fQN8d0XBqF6AIgoXSTERq13dxsBjGHUKW6jwNwTsXTCjQPDL3ECPx9THc82WyPk1DxBmOBypeBmNGFBy1chYcUwcFGgkUFJ8rGVL0M7Z4NoW94W9njM9Ro6nq6qi01N_siJXZ46oOsi5HbyexljfcOFZeQ1mWyaHckOPpgQBsjWVxXc0Af7K47Ot1UNvND8V0XtemOjQsrXOfBKJe0gp87bj9rlU2Tu9-VMS0kdi0lqXzDYJQrSqVkmPuM4w; GPS=1; VISITOR_INFO1_LIVE=nf5I4vF2akE; VISITOR_PRIVACY_METADATA=CgJJRBIEGgAgJA%3D%3D; __Secure-1PSIDTS=sidts-CjQB7I_69Hz3P1cV_dfTILaieu_5-kHNTv_Tq7hP_DLxXp7o6gJ9OrEDPM5T2pU2lbkWKTPVEAA; __Secure-3PSIDTS=sidts-CjQB7I_69Hz3P1cV_dfTILaieu_5-kHNTv_Tq7hP_DLxXp7o6gJ9OrEDPM5T2pU2lbkWKTPVEAA; HSID=ANM-CYjrWIxtAYHkw; SSID=AK-kom9-R9ubRd_Q7; APISID=chavYjlrUE3rUqIl/A3oRfXvENZARU6fKj; SAPISID=TE-eZVZtTpK8W2I8/AsLTcB28YYRUWCdKk; __Secure-1PAPISID=TE-eZVZtTpK8W2I8/AsLTcB28YYRUWCdKk; __Secure-3PAPISID=TE-eZVZtTpK8W2I8/AsLTcB28YYRUWCdKk; SID=g.a0006ghbvApF3RVC7H-qLglHKn1wsVv9-e6lYNx1axSWb5M70l6jChzWnL3iJbqYxKQZSskEpAACgYKAVcSARISFQHGX2MiASqgXDm-QAIm2KpWdMN26RoVAUF8yKp4zkE6BQtH_ojBkydl-t-b0076; __Secure-1PSID=g.a0006ghbvApF3RVC7H-qLglHKn1wsVv9-e6lYNx1axSWb5M70l6jqvIR5RKQCDcOV117ark3uQACgYKAeQSARISFQHGX2MildQ-kTRWi0rJK22rG2h4ZRoVAUF8yKoMMnaWWYk5O1Ay0oGylp-I0076; __Secure-3PSID=g.a0006ghbvApF3RVC7H-qLglHKn1wsVv9-e6lYNx1axSWb5M70l6jmWCMsMBjRAvMJ2fOrLkPSwACgYKAXcSARISFQHGX2MiAY8pCT3Wgh2DAKUhKmkiehoVAUF8yKr6alMIIA5wG3-QzMwmdJ1J0076; __Secure-ROLLOUT_TOKEN=CKeSu4j-ytr7pAEQ3LyVpJHPkgMYyY-MwJHPkgM%3D; PREF=f6=40000000&tz=Asia.Jakarta; SIDCC=AKEyXzV44D_aYJFQgi2UQP9hvCSL6KpcVrwwUxE4WcSffbneyM9HldLWmjqbo99qTBeV-h3b; __Secure-1PSIDCC=AKEyXzVTaza06E7899wE0SmWQWmOTHjkKWU_z9Cwt1XxdgH4mZKqyIH-OmAPueIMAc61bylf; __Secure-3PSIDCC=AKEyXzVWQ9ixy_xKJsf_v63u0S5CjhDx8fkIdJdNnZ6oi_N35730ELtgpeBsjT4AwoO5ui6Wig"

def get_ydl_opts():
    return {
        # Kita buat pencarian format jadi lebih fleksibel biar nggak kena 'format not available'
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'geo_bypass': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Cookie': MY_COOKIE,
            'Accept': '*/*',
        }
    }

@app.get("/api/download")
async def download(url: str = Query(...)):
    try:
        # Pake opsi pencarian format yang paling luas
        ydl_opts = {
            'format': 'ba/b', # Ambil audio apapun yang ada
            'quiet': True,
            'cookiefile': None,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Cookie': MY_COOKIE
            }
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "success": True,
                "title": info.get('title'),
                "data": info.get('url'),
                "format": "mp3"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bypass Gagal: {str(e)}")
