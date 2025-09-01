import requests

# Asegúrate de que el servidor Flask esté corriendo en http://127.0.0.1:5000
url = "http://127.0.0.1:5000/process"

# Cambia "Esports World Cup" por el canal que quieras probar
data = {"channel_name": "Esports World Cup"}

try:
    print("[INFO] Enviando request a /process...")
    res = requests.post(url, json=data, timeout=300)  # Timeout largo por audio/transcribe
    res.raise_for_status()  # Lanza HTTPError si status != 200

    try:
        response_json = res.json()
        print("[INFO] Respuesta /process:", response_json)
    except ValueError:
        print("[ERROR] No se pudo decodificar JSON. Texto recibido:", res.text)

except requests.exceptions.HTTPError as e:
    print("[HTTPError]", e, res.text)
except requests.exceptions.ConnectionError as e:
    print("[ERROR] No se pudo conectar al servidor:", e)
except requests.exceptions.Timeout as e:
    print("[ERROR] Timeout en la request:", e)
except Exception as e:
    print("[ERROR] Otro error:", e)
