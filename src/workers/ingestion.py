# src/workers/ingestion.py
import warnings
warnings.filterwarnings("ignore")

from pathlib import Path
from loguru import logger
from inngest import Inngest, Event

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from src.core.config import configure_llamaindex
from src.core.qdrant_store import configure_qdrant

inngest = Inngest(app_id="wiidcos")
import uuid
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter

# inside ingest_document(event): (decorator version)
def ingest_document(event):
    data = event.data
    file_path = data["path"]
    file_name = data["filename"]

    configure_llamaindex(temperature=0.1)
    _, store = configure_qdrant()

    # ✅ create a unique doc_id for this file
    doc_id = str(uuid.uuid4())

    logger.info(f"📥 Starting ingestion for {file_name} (doc_id={doc_id})")

    # Load raw docs
    docs = SimpleDirectoryReader(input_files=[file_path]).load_data()

    # ✅ Attach metadata on each Document
    for d in docs:
        d.metadata = d.metadata or {}
        d.metadata.update({"doc_id": doc_id, "source": file_name})

    # (optional) custom chunking, keeps metadata
    splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
    nodes = splitter.get_nodes_from_documents(docs)

    storage_context = StorageContext.from_defaults(vector_store=store)
    index = VectorStoreIndex(nodes, storage_context=storage_context)

    # Persist index structure (optional local)
    index.storage_context.persist(persist_dir="./storage/qdrant")

    logger.success(f"✅ Completed ingestion for {file_name} (doc_id={doc_id})")
    return {"status": "completed", "filename": file_name, "doc_id": doc_id}


if __name__ == "__main__":
    # ...existing code...
    configure_llamaindex(temperature=0.1)
    _, store = configure_qdrant()
    for file in pdf_files:
        doc_id = str(uuid.uuid4())
        logger.info(f"Processing {file.name} (doc_id={doc_id})")

        docs = SimpleDirectoryReader(input_files=[str(file)]).load_data()
        for d in docs:
            d.metadata = d.metadata or {}
            d.metadata.update({"doc_id": doc_id, "source": file.name})

        splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
        nodes = splitter.get_nodes_from_documents(docs)

        storage_context = StorageContext.from_defaults(vector_store=store)
        index = VectorStoreIndex(nodes, storage_context=storage_context)
        index.storage_context.persist(persist_dir="./storage/qdrant")

        logger.success(f"✅ Completed ingestion for {file.name} (doc_id={doc_id})")