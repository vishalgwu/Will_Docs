import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

from loguru import logger
from typing import Optional

from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.vector_stores.types import MetadataFilters, ExactMatchFilter

from src.core.qdrant_store import configure_qdrant
from src.core.config import configure_llamaindex

def query_qdrant(query: str, top_k: int = 3, doc_id: Optional[str] = None, source: Optional[str] = None):
    """Query vectors stored in Qdrant via LlamaIndex, optionally scoped to a doc_id or source (filename)."""
    configure_llamaindex(temperature=0.1)
    _, store = configure_qdrant()

    index = VectorStoreIndex.from_vector_store(store)

    filters = None
    if doc_id:
        filters = MetadataFilters(filters=[ExactMatchFilter(key="doc_id", value=doc_id)])
    elif source:
        filters = MetadataFilters(filters=[ExactMatchFilter(key="source", value=source)])

    synth = get_response_synthesizer(response_mode="compact")
    # ✅ pass filters so retriever only looks at that document's chunks
    query_engine = index.as_query_engine(
        similarity_top_k=top_k,
        response_synthesizer=synth,
        filters=filters
    )
    response = query_engine.query(query)

    logger.info(f"🧠 Query: {query}  | doc_id={doc_id} source={source}")
    logger.info(f"💡 Answer: {response}")
    print(f"\nAnswer:\n{response}\n")
    return str(response)

if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "What is this PDF about?"
    query_qdrant(q)
