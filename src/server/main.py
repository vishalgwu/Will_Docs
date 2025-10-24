from fastapi import FastAPI, UploadFile, File
from src.core.config import configure_llamaindex
from src.core.qdrant_store import configure_qdrant
from inngest import Inngest
import os

app = FastAPI(title="WiiDcos API v2")
inngest = Inngest(app_id="wiidcos")

UPLOAD_DIR = "./Data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
def startup():
    configure_llamaindex(temperature=0.1)
    configure_qdrant()

@app.get("/healthz")
def health_check():
    return {"status": "ok"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as f:
        f.write(await file.read())
    await inngest.send("doc/ingest.requested", data={"filename": file.filename, "path": path})
    return {"message": f"{file.filename} queued for ingestion."}
