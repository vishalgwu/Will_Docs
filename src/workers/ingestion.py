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

@inngest.create_function(
    fn_id="ingest_document",
    trigger=Event(name="doc/ingest.requested")
)
def ingest_document(event):
    data = event.data
    file_path = data["path"]
    file_name = data["filename"]

    configure_llamaindex(temperature=0.1)
    _, store = configure_qdrant()

    logger.info(f"📥 Starting ingestion for {file_name}")
    docs = SimpleDirectoryReader(input_files=[file_path]).load_data()

    # ✅ Explicitly attach Qdrant via StorageContext
    storage_context = StorageContext.from_defaults(vector_store=store)
    index = VectorStoreIndex.from_documents(docs, storage_context=storage_context)

    # ✅ Persist index structure (optional)
    index.storage_context.persist(persist_dir="./storage/qdrant")

    logger.success(f"✅ Completed ingestion for {file_name}")
    return {"status": "completed", "filename": file_name}


if __name__ == "__main__":
    uploads_dir = Path("./Data/uploads")
    pdf_files = list(uploads_dir.glob("*.pdf"))

    if not pdf_files:
        logger.warning("⚠️ No PDFs found in Data/uploads!")
    else:
        configure_llamaindex(temperature=0.1)
        _, store = configure_qdrant()
        for file in pdf_files:
            logger.info(f"Processing {file.name}")
            docs = SimpleDirectoryReader(input_files=[str(file)]).load_data()

            # ✅ Explicit StorageContext ensures embeddings are pushed to Qdrant
            storage_context = StorageContext.from_defaults(vector_store=store)
            index = VectorStoreIndex.from_documents(docs, storage_context=storage_context)
            index.storage_context.persist(persist_dir="./storage/qdrant")

            logger.success(f"✅ Completed ingestion for {file.name}")
