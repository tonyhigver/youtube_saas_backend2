import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

# Cargar .env desde la raíz del proyecto
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

INDEX_NAME = "youtube-chunks"

# Crear índice si no existe
if INDEX_NAME not in pc.list_indexes().names():
    print(f"[INFO] Creando índice {INDEX_NAME}")
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,  # all-MiniLM-L6-v2 → 384 dimensiones
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
else:
    print(f"[INFO] Índice {INDEX_NAME} ya existe")

index = pc.Index(INDEX_NAME)
