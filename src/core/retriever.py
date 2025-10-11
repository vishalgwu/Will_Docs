# src/core/retriever.py
import os
import warnings
from dotenv import load_dotenv
from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.node_parser import SentenceSplitter

warnings.filterwarnings("ignore", category=UserWarning)
load_dotenv()

# ----------------------------------------------------------
# Load persisted index
# ----------------------------------------------------------
def load_index(persist_dir: str = None):
    """Load the vector index from local storage."""
    if persist_dir is None:
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        persist_dir = os.path.join(root_dir, "storage", "index")

    if not os.path.exists(persist_dir):
        raise FileNotFoundError(f"❌ Index not found at {persist_dir}")

    storage = StorageContext.from_defaults(persist_dir=persist_dir)
    return load_index_from_storage(storage)

# ----------------------------------------------------------
# Advanced Query Function
# ----------------------------------------------------------
def advanced_query(
    query_text: str,
    mode: str = "default",
    top_k: int = 4,
    stream: bool = False,
    re_rank: bool = True
):
    """
    Execute an advanced query against the local vector index.
    Supports summarization, keyword extraction, and re-ranking.
    """
    print("🔍 Loading index...")
    index = load_index()

    # Optional: fine-tune chunking logic globally
    Settings.text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)

    retriever = VectorIndexRetriever(index=index, similarity_top_k=top_k)

    # optional LLM-based reranker
    if re_rank:
        print("🔧 Attempting LLM-based reranker...")
        try:
            # Works only if llama_index.postprocessor is available
            from llama_index.postprocessor.rerank import LLMRerank
            reranker = LLMRerank(top_n=top_k)
            Settings.node_postprocessors = [reranker]
            print("✅ Reranker enabled.")
        except Exception as e:
            print(f"⚠️  Reranker unavailable: {e}")
            Settings.node_postprocessors = []

    # ✅ define the missing synthesizer
    synthesizer = get_response_synthesizer(response_mode="tree_summarize")

    # Build query engine
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=synthesizer,
        streaming=stream,
    )

    # Adjust query style based on mode
    if mode == "summary":
        query_text = f"Summarize the document with focus on: {query_text}"
    elif mode == "keyword":
        query_text = f"List key terms and entities related to: {query_text}"

    print(f"🚀 Running query: {query_text}")
    response = query_engine.query(query_text)

    # Extract metadata for sources
    sources = []
    for node in getattr(response, "source_nodes", []):
        meta = node.node.metadata
        filename = meta.get("file_name", "unknown")
        page = meta.get("page_label", "")
        sources.append(f"{filename} {page}".strip())

    result = {
        "answer": str(response),
        "sources": list(set(sources)),
        "score": getattr(response, "score", None)
    }

    print("\n✅ Query completed.")
    print("🧠 Answer:\n", result["answer"])
    print("\n📚 Sources:", result["sources"])
    return result


# ----------------------------------------------------------
# CLI entry
# ----------------------------------------------------------
if __name__ == "__main__":
    q = input("Enter your query: ")
    advanced_query(q, mode="default", top_k=3)
