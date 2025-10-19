# src/core/retriever.py
from llama_index.core import VectorStoreIndex
from src.core.qdrant_store import configure_qdrant
from src.core.config import configure_llamaindex
from loguru import logger
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)


def query_qdrant(query: str, top_k: int = 3):
    """Query vectors stored in Qdrant via LlamaIndex."""
    configure_llamaindex(temperature=0.1)
    _, store = configure_qdrant()

    # ✅ Create index from Qdrant vector store
    index = VectorStoreIndex.from_vector_store(store)

    # ✅ Create query engine (retriever + response synthesizer)
    query_engine = index.as_query_engine(similarity_top_k=top_k, response_mode="compact")

    # ✅ Run the query
    response = query_engine.query(query)
    logger.info(f"🧠 Query: {query}")
    logger.info(f"💡 Answer: {response}")

    print(f"\nAnswer:\n{response}\n")
    return str(response)


if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "What is this PDF about?"
    query_qdrant(query)
