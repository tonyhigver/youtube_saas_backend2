import yt_dlp
import re

def sanitize_filename(s):
    # Elimina caracteres que no se permiten en nombres de archivo
    return re.sub(r'[\\/*?:"<>|]', "", s)

def download_audio(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',  # Nombre temporal antes de convertir
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',      # Extrae a mp3
            'preferredquality': '192',    # Calidad 192kbps
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = sanitize_filename(info['title']) + ".mp3"
            print(f"[DEBUG] Audio descargado a: {filename}")
            return filename
    except Exception as e:
        print(f"[ERROR] Falló download_audio: {e}")
        raise
