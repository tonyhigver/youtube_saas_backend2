import yt_dlp
import re
import os

def sanitize_filename(s):
    # Elimina caracteres que no se permiten en nombres de archivo
    return re.sub(r'[\\/*?:"<>|]', "", s)

def download_audio(video_url):
    # Crear carpeta audio si no existe
    os.makedirs("audio", exist_ok=True)

    # Ruta final donde guardaremos el audio
    audio_path = os.path.join("audio", "%(id)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",  # audio más liviano
        "outtmpl": audio_path,
        "noplaylist": True,
        "concurrent_fragment_downloads": 1,  # menos uso de RAM
        "cookiefile": "youtube_cookies.txt",  # <-- archivo de cookies
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "128",  # calidad más baja que 192 → menos peso
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = os.path.join("audio", sanitize_filename(info['title']) + ".mp3")
            print(f"[DEBUG] Audio descargado a: {filename}")
            return filename
    except Exception as e:
        print(f"[ERROR] Falló download_audio: {e}")
        raise
