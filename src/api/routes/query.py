from fastapi import APIRouter, Query
from loguru import logger
from src.core.retriever import query_qdrant

router = APIRouter(prefix="/query", tags=["Query"])


@router.get("/")
async def query_docs(q: str = Query(..., description="Your question")):
    """Query indexed PDFs"""
    logger.info(f"🔍 Query received: {q}")
    answer = query_qdrant(q)
    return {"query": q, "answer": answer}
