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


def load_index(persist_dir: str = None):
    if persist_dir is None:
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        persist_dir = os.path.join(root_dir, "storage", "index")

    if not os.path.exists(persist_dir):
        raise FileNotFoundError(f" Index not found at {persist_dir}")

    storage = StorageContext.from_defaults(persist_dir=persist_dir)
    index = load_index_from_storage(storage)
    print(f" Index loaded from {persist_dir}")
    return index



def advanced_query(
    query_text: str,
    mode: str = "default",
    top_k: int = 4,
    stream: bool = False,
    re_rank: bool = True
):

    print(" Loading index...")
    index = load_index()

    # Global settings
    Settings.text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)

    retriever = VectorIndexRetriever(index=index, similarity_top_k=top_k)

    # Try enabling LLM re-ranking
    if re_rank:
        print(" Attempting LLM-based reranker...")
        try:
            #  Correct import path for new LlamaIndex versions
            from llama_index.core.postprocessor import LLMRerank
            reranker = LLMRerank(top_n=top_k)
            Settings.node_postprocessors = [reranker]
            print(" LLM-based reranker enabled.")
        except Exception as e:
            print(f" Reranker unavailable: {e}")
            Settings.node_postprocessors = []

    # Choose a synthesis style
    synthesizer = get_response_synthesizer(response_mode="tree_summarize")

    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=synthesizer
    )

    # Adjust mode-based query prompt
    if mode == "summary":
        query_text = f"Summarize the document focusing on: {query_text}"
    elif mode == "keyword":
        query_text = f"List key technical concepts or terms related to: {query_text}"

    print(f"\n Running query:\n{query_text}\n")
    response = query_engine.query(query_text)

    # Collect metadata
    sources = []
    for node in getattr(response, "source_nodes", []):
        meta = node.node.metadata
        filename = meta.get("file_name", "unknown")
        page = meta.get("page_label", "")
        sources.append(f"{filename} {page}".strip())

    result = {
        "answer": str(response),
        "sources": sorted(list(set(sources))),
        "confidence": getattr(response, "score", None)
    }

    print(" Query completed.\n")
    print(" Answer:\n", result["answer"]) 
    print("\n Sources:", result["sources"])
    if result["confidence"]:
        print(f"\n Confidence: {result['confidence']:.2f}")

    return result


if __name__ == "__main__":
    q = input("Enter your query: ")
    advanced_query(q, mode="default", top_k=3)


