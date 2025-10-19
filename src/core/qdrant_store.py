from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import Settings

def configure_qdrant(collection="wiidcos_docs", host="localhost", port=6333):

    client = QdrantClient(host=host, port=port)
    vs = QdrantVectorStore(client=client, collection_name=collection)
    Settings.vector_store = vs
    print(f"Qdrant connected at {host}:{port}, collection={collection}")
    return client, vs