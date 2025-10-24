# src/core/qdrant_store.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import Settings
from loguru import logger

COLLECTION = "wiidcos_docs"
DIM = 1536  # text-embedding-3-small
DIST = Distance.COSINE

def configure_qdrant(collection: str = COLLECTION, host: str = "localhost", port: int = 6333):
    client = QdrantClient(host=host, port=port)

    # Ensure collection exists; create if missing
    try:
        client.get_collection(collection_name=collection)
        logger.info(f"Qdrant: collection '{collection}' already exists.")
    except Exception:
        logger.info(f"Qdrant: creating collection '{collection}' with dim={DIM}, distance={DIST}.")
        client.recreate_collection(
            collection_name=collection,
            vectors_config=VectorParams(size=DIM, distance=DIST),
        )

    store = QdrantVectorStore(client=client, collection_name=collection)
    Settings.vector_store = store
    logger.info(f" Qdrant connected: {host}:{port}, collection={collection}")
    return client, store
