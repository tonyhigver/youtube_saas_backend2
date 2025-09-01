import yt_dlp
import re
import os

def sanitize_filename(s):
    # Elimina caracteres que no se permiten en nombres de archivo
    return re.sub(r'[\\/*?:"<>|]', "", s)

def download_audio(video_url):
    # Crear carpeta audio si no existe
    os.makedirs("audio", exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio/%(id)s.%(ext)s',  # Guardar en carpeta audio
        'quiet': False,
        'cookiefile': 'youtube_cookies.txt',  # <-- tu archivo de cookies
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
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
