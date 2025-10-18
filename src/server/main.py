# src/server/main.py
# src/server/main.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastapi import FastAPI
from src.core.config import configure_llamaindex

app = FastAPI(title="WiiDcos API")

@app.on_event("startup")
def _startup():
    configure_llamaindex(temperature=0.1)
    print("✅ Server started and LlamaIndex configured")

@app.get("/healthz")
def health_check():
    return {"status": "ok"}
