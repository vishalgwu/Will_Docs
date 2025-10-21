#  WiiDcos RAG — Chat with Your PDFs

Hello 

Welcome to **WiiDcos**, a full-stack local **RAG (Retrieval-Augmented Generation)** system — built from scratch with **LlamaIndex + Qdrant + FastAPI + Streamlit + Docker**.

This project started life as a "hello-production-RAG" experiment — a way of sewing together the moving parts of how ChatGPT-style apps read documents and answer questions intelligently. Now it's a full-stack system that can take in PDFs, index them in a vector database, and enable you to chat with them directly in your browser. ????

---
##  Tech Stack

| Layer | Tools / Frameworks | Description |
|-------|--------------------|--------------|
|  Core AI | **LlamaIndex**, **OpenAI Embeddings**, **Qdrant** | Text chunking, embedding, and semantic search |
| ️ Backend | **FastAPI** | REST API for upload + query |
|  Frontend | **Streamlit** | Clean UI for drag-and-drop & chat |
|  Infra | **Docker** | Containerized local Qdrant DB |
|  Langs | **Python 3.10+** | Written cleanly in modular `src/` layout |

---

##  Folder Structure

```
WiiDcos/
├── Data/
│   └── uploads/                  # uploaded PDFs live here
├── docker/
│   └── docker-compose.yml        # Qdrant container setup
├── src/
│   ├── api/                      # FastAPI backend
│   │   ├── main.py
│   │   └── routes/
│   │        ├── upload.py
│   │        └── query.py
│   ├── core/                     # core configs & logic
│   │   ├── config.py
│   │   ├── qdrant_store.py
│   │   └── retriever.py
│   ├── workers/                  # ingestion jobs
│   │   └── ingestion.py
│   └── ui/                       # streamlit front-end
│        └── app.py
├── .env                  # store your API keys here
├── requirements.txt
└── README.md
```

---
## How It Works

1️ **PDF Upload → Ingestion**

- Upload a PDF through the Streamlit UI or call the backend `/upload` route.
- Document is stored in `Data/uploads/`.
- **LlamaIndex** reads and chunks the document.
- **OpenAI Embeddings** (or any embedding model) converts chunks to vector embeddings.
- **Qdrant** stores the vectors for semantic retrieval efficiently.

2️ **Query → Retrieval + Answer**

- User provides a query in the chat interface.
- Top-k most similar chunks are retrieved from Qdrant by the system based on semantic similarity.
- Retrieved chunks are passed as context to an LLM (OpenAI or other) with low temperature: 0.1–0.2.
- The LLM generates a grounded, relevant answer that quotes or utilizes the retrieved chunks.

3️ **Local-first architecture**

- Qdrant is executed locally in Docker.
- PDFs and indexes are stored locally to disk.
- Only embedding calls and LLM calls get sent out to external APIs (unless you flip to fully local models).

---
##  Setup Guide (Windows + Conda)

These commands are tested for local development. Adjust the commands for macOS / Linux if necessary.

### 1️ Clone the repo

```bash
git clone https://github.com/<your-username>/WiiDcos.git
cd WiiDcos
```

### 2️ Create & activate the environment

```bash
conda create -n willdocs python=3.10 -y
conda activate willdocs
```

### 3️ Install dependencies

```bash
pip install -r req.txt
```

### 4️ Configure environment variables

Create a `.env` file in project root and insert your API keys (example):

```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
# OPTIONAL:
# QDRANT_URL=http://localhost:6333
# QDRANT_API_KEY=your_qdrant_key_if_any
```



---

## Run Qdrant (Docker)

```bash
cd docker
docker compose up -d
```

Open the Qdrant dashboard at: `http://localhost:6333/dashboard`

---

## Start the FastAPI backend

From project root:

```bash
uvicorn src.api.main:app --reload --port 8000
```

Open the API docs at: `http://127.0.0.1:8000/docs`

Routes you should expect:
- `POST /upload` — Accepts PDF uploads and triggers ingestion
- `GET /query` — Query the indexed documents (or `POST /query` depending on implementation)

---

## Launch the Streamlit UI

```bash
streamlit run src/ui/app.py
```

Open the UI at: `http://localhost:8501`

Typical flow:
- Drag & drop a PDF
- Wait for " Uploaded & indexed"
- Ask: "What is this PDF about?"
- Receive a short, sourced answer

---
##  Example

**Query:**

```
What is this PDF about?
```

**Answer (example):**

```
The PDF is regarding some research papers and studies on speech separation using deep learning, transformer, RNN, and LSTM models.
```

---
##  Optional Improvements (Next Steps)

- **Chat History** — Store chat sessions for greater continuity in the UI.
- **Streaming Responses** — Offer streaming token-by-token output for a ChatGPT-like experience.
- **Multi-PDF Support** — Index multiple PDFs and enable users to choose which document(s) to query.
- **Offline Embeddings** — Replace OpenAI embeddings with offline sentence-transformers to reduce API usage.
- **Full Docker Compose** — Add FastAPI + Streamlit services in `docker-compose` for one-command runs.
- **Model Flexibility** — Add a config toggle to alternate between OpenAI and local LLMs (e.g., Llama 2 family).

---
##  Troubleshooting

- **Qdrant unreachable:** Ensure Docker container running and ports open (default `6333`).
- **Embedding errors:** Ensure your `OPENAI_API_KEY` is valid and has quota. Use local embeddings if rate-limited.
- **Slow indexing:** Chunk size and overlap settings control speed vs. retrieval quality. Modify in `src/core/retriever.py` or LlamaIndex settings.

## Deployment notes

- For quick sharing, you can deploy the Streamlit app to [Streamlit Cloud] or the backend to services like Render or Railway.
- For production, remember: managed vector DB (Qdrant Cloud), secrets management, HTTPS, authentication, and rate-limiting.

---

## Recommended `requirements.txt` (example)

Starting `requirements.txt` snippet. Pin versions to what you've locally tested.

```
fastapi>=0.95
uvicorn[standard]>=0.22
streamlit>=1.25
qdrant-client>=1.2
llama-index>=0.8
openai>=0.27
python-dotenv>=1.0
pydantic>=1.10
pandas>=1.5
tqdm>=4.64
pdfminer.six>=20221105
sentence-transformers>=2.2
```

Bump package versions for compatibility with your environment.

---

## Credits

- **LlamaIndex**
- **Qdrant**
- **FastAPI**
- **Streamlit**
- **OpenAI**

## TL;DR

WiiDcos RAG = Upload PDFs → Store in Qdrant → Query via LlamaIndex → Answer with OpenAI → Chat via Streamlit.

A small but end-to-end production-ready RAG stack, built with logs, tests, and plenty of debugging.

**Author:** Vishal Fulsundar
M.S. Data Science — The George Washington University


---
