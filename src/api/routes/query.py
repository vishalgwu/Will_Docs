from fastapi import APIRouter, Query
from typing import Optional
from loguru import logger
from src.core.retriever import query_qdrant

router = APIRouter(prefix="/query", tags=["Query"])

@router.get("/")
async def query_docs(
    q: str = Query(..., description="Your question"),
    doc_id: Optional[str] = Query(default=None, description="Optional doc_id to scope search"),
    source: Optional[str] = Query(default=None, description="Optional filename to scope search"),
    top_k: int = Query(default=3, ge=1, le=20)
):
    """Query indexed PDFs, optionally restricted to a specific doc via doc_id or source (filename)."""
    logger.info(f"🔍 Query received: {q} | doc_id={doc_id} | source={source}")
    answer = query_qdrant(q, top_k=top_k, doc_id=doc_id, source=source)
    return {"query": q, "answer": answer, "doc_id": doc_id, "source": source}
