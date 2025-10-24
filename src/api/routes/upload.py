from fastapi import APIRouter, UploadFile, File
from loguru import logger
from pathlib import Path
import uuid

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from src.core.config import configure_llamaindex
from src.core.qdrant_store import configure_qdrant

router = APIRouter(prefix="/upload", tags=["Upload"])
UPLOAD_DIR = Path("Data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    """Upload and ingest a PDF into Qdrant; returns doc_id."""
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())
    logger.info(f"📄 Received file: {file_path}")

    configure_llamaindex(temperature=0.1)
    _, store = configure_qdrant()

    # unique doc_id for this file
    doc_id = str(uuid.uuid4())

    docs = SimpleDirectoryReader(input_files=[str(file_path)]).load_data()
    for d in docs:
        d.metadata = d.metadata or {}
        d.metadata.update({"doc_id": doc_id, "source": file.filename})

    splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
    nodes = splitter.get_nodes_from_documents(docs)

    storage_context = StorageContext.from_defaults(vector_store=store)
    index = VectorStoreIndex(nodes, storage_context=storage_context)
    index.storage_context.persist(persist_dir="./storage/qdrant")

    logger.success(f"✅ {file.filename} ingested successfully (doc_id={doc_id}).")
    return {"status": "success", "filename": file.filename, "doc_id": doc_id}
