# utils/embeddings.py

model = None

def get_model():
    """
    Devuelve el modelo de embeddings.
    Solo lo carga la primera vez que se llama.
    """
    global model
    if model is None:
        print("DEBUG: Cargando modelo de embeddings por primera vez...")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

def generate_embeddings(text, is_query=False):
    model = get_model()  # <-- aquí se carga solo si no estaba cargado

    if is_query:
        embedding = model.encode(text).tolist()
        print(f"DEBUG embedding length (query): {len(embedding)}")
        return [{"embedding": embedding}]
    
    chunks = chunk_text(text)
    embeddings = model.encode(chunks).tolist()

    # debug cada chunk
    for i, e in enumerate(embeddings):
        print(f"DEBUG embedding length chunk {i}: {len(e)}")
    
    return [{"text": c, "embedding": e} for c, e in zip(chunks, embeddings)]
