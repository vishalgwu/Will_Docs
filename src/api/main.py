from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import upload, query

app = FastAPI(title="WiiDcos RAG API", version="1.0")

# Allow Streamlit / localhost requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(upload.router)
app.include_router(query.router)


@app.get("/")
def root():
    return {"message": "WiiDcos RAG API is running 🚀"}
