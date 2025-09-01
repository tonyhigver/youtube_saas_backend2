import os
import requests
from dotenv import load_dotenv

# 👇 Cargar variables de entorno desde la raíz del proyecto
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_channel_id(channel_name):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={channel_name}&key={YOUTUBE_API_KEY}&type=channel"
    res = requests.get(url).json()
    print("DEBUG get_channel_id response:", res)  # debug
    if "items" not in res or not res["items"]:
        raise ValueError(f"No se pudo obtener el canal: {res}")
    return res['items'][0]['snippet']['channelId']

def get_latest_video_url(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&maxResults=1&order=date&key={YOUTUBE_API_KEY}"
    res = requests.get(url).json()
    print("DEBUG get_latest_video_url response:", res)  # debug
    if "items" not in res or not res['items']:
        raise ValueError(f"No se pudo obtener el último video: {res}")
    video_id = res['items'][0]['id']['videoId']
    return f"https://www.youtube.com/watch?v={video_id}"
