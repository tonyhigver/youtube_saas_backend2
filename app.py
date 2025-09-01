from flask import Flask, request, jsonify
from utils.youtube import get_channel_id, get_latest_video_url
from utils.audio import download_audio
from utils.transcribe import transcribe_audio
from utils.embeddings import generate_embeddings
from utils.pinecone_utils import index

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_channel():
    try:
        channel_name = request.json.get("channel_name")
        if not channel_name:
            return jsonify({"error": "No channel_name provided"}), 400

        print(f"[INFO] Procesando canal: {channel_name}")

        # Paso 1: obtener channel_id
        channel_id = get_channel_id(channel_name)
        print(f"[DEBUG] Channel ID obtenido: {channel_id}")

        # Paso 2: obtener último video
        video_url = get_latest_video_url(channel_id)
        print(f"[DEBUG] Último video URL: {video_url}")

        # Paso 3: descargar audio
        audio_path = download_audio(video_url)
        print(f"[DEBUG] Audio descargado en: {audio_path}")

        # Paso 4: transcribir audio
        text = transcribe_audio(audio_path)
        print(f"[DEBUG] Texto transcrito (primeros 200 chars): {text[:200]}...")

        # Paso 5: generar embeddings
        chunks = generate_embeddings(text)
        print(f"[DEBUG] Número de chunks generados: {len(chunks)}")
        if len(chunks) > 0:
            print(f"[DEBUG] Longitud primer embedding: {len(chunks[0]['embedding'])}")

        # Paso 6: subir a Pinecone
        for i, chunk in enumerate(chunks):
            try:
                index.upsert([(f"{channel_id}_{i}", chunk["embedding"], {"text": chunk["text"]})])
            except Exception as e:
                print(f"[ERROR] Falló upsert chunk {i}: {e}")
        print("[INFO] Chunks subidos a Pinecone")

        return jsonify({"status": "ok"})

    except Exception as e:
        print("[ERROR] Error en /process:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/search", methods=["POST"])
def search_query():
    try:
        query = request.json.get("query")
        if not query:
            return jsonify({"error": "No query provided"}), 400

        print(f"[INFO] Buscando: {query}")

        # Generar embedding de la query
        embedding = generate_embeddings(query, is_query=True)[0]["embedding"]
        print(f"[DEBUG] Longitud embedding de la query: {len(embedding)}")

        # Consultar Pinecone
        results = index.query(embedding, top_k=5, include_metadata=True)
        chunks = [item["metadata"]["text"] for item in results["matches"]]
        print(f"[INFO] Chunks encontrados: {len(chunks)}")

        return jsonify({"chunks": chunks})

    except Exception as e:
        print("[ERROR] Error en /search:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
