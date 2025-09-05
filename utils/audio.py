import yt_dlp
import re
import os
from datetime import datetime

def sanitize_filename(s):
    """
    Limpia el nombre del archivo eliminando caracteres no permitidos.
    """
    return re.sub(r'[\\/*?:"<>|]', "", s)

def download_audio(video_url):
    """
    Descarga el audio de un video de YouTube usando yt-dlp,
    utilizando cookies para autenticar la sesión.
    """
    # Carpeta base para guardar audios
    base_dir = "audio"
    os.makedirs(base_dir, exist_ok=True)

    # Ruta de archivo de cookies (asegúrate que este archivo exista y tenga permisos correctos)
    cookies_path = "/opt/browserless/chrome-data/cookies.txt"

    # Plantilla de nombre de archivo: ID del video + extensión
    audio_path_template = os.path.join(base_dir, "%(id)s.%(ext)s")

    # Opciones de yt-dlp
    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",  # audio más ligero
        "outtmpl": audio_path_template,
        "noplaylist": True,
        "concurrent_fragment_downloads": 1,  # menos uso de RAM
        "cookiefile": cookies_path,  # <-- archivo de cookies persistente
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",  # buena calidad sin ocupar demasiado
        }],
        "quiet": False,  # para ver progreso en consola
        "no_warnings": True,
        "progress_hooks": [lambda d: print(f"[DEBUG] {d}")],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            # Nombre final del archivo
            filename = os.path.join(base_dir, sanitize_filename(info['title']) + ".mp3")
            print(f"[INFO] Audio descargado a: {filename}")
            return filename
    except Exception as e:
        print(f"[ERROR] Falló download_audio: {e}")
        raise

# Ejemplo de uso (puedes borrar o comentar al integrar con tu frontend)
if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=VIDEO_ID"
    download_audio(test_url)
