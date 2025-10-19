from fastapi import APIRouter, UploadFile, File
from loguru import logger
from pathlib import Path
from src.workers.ingestion import configure_llamaindex, configure_qdrant
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = Path("Data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    """Upload and ingest a PDF into Qdrant"""
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())
    logger.info(f"📄 Received file: {file_path}")

    # Ingest into Qdrant
    configure_llamaindex(temperature=0.1)
    _, store = configure_qdrant()

    docs = SimpleDirectoryReader(input_files=[str(file_path)]).load_data()
    storage_context = StorageContext.from_defaults(vector_store=store)
    index = VectorStoreIndex.from_documents(docs, storage_context=storage_context)
    index.storage_context.persist(persist_dir="./storage/qdrant")

    logger.success(f"✅ {file.filename} ingested successfully.")
    return {"status": "success", "filename": file.filename}
