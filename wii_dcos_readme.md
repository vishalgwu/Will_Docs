# 🧠 WiiDcos RAG — Chat With Your PDFs

Hey there 👋

Welcome to **WiiDcos**, a fully local **RAG (Retrieval-Augmented Generation)** system — built from scratch using **LlamaIndex + Qdrant + FastAPI + Streamlit + Docker**.

This project started as a "hello-production-RAG" experiment — a way to connect the moving parts behind how ChatGPT-style apps read documents and answer questions intelligently. Now it’s a full-stack system that can ingest PDFs, store them in a vector database, and let you chat with them right from your browser. 🚀

---

## ⚙️ Tech Stack

| Layer | Tools / Frameworks | Description |
|-------|--------------------|--------------|
| 🧩 Core AI | **LlamaIndex**, **OpenAI Embeddings**, **Qdrant** | Text chunking, embedding, and semantic search |
| 🖥️ Backend | **FastAPI** | REST API for upload + query |
| 💬 Frontend | **Streamlit** | Clean UI for drag-and-drop & chat |
| 🧰 Infra | **Docker** | Containerized local Qdrant DB |
| 🔧 Langs | **Python 3.10+** | Written cleanly in modular `src/` layout |

---

## 🧱 Folder Structure

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
├── .env                          # keep your API keys here
├── requirements.txt
└── README.md
```

---

## 🚀 How It Works

1️⃣ **PDF Upload → Ingestion**

- Upload a PDF through the Streamlit UI or call the backend `/upload` route.
- The file is saved to `Data/uploads/`.
- **LlamaIndex** reads and chunks the document.
- **OpenAI Embeddings** (or another embedding model) converts chunks into vector embeddings.
- **Qdrant** stores the vectors for fast semantic retrieval.

2️⃣ **Query → Retrieval + Answer**

- User types a query in the chat UI.
- The system retrieves the top-k most relevant chunks from Qdrant using semantic similarity.
- Retrieved chunks are passed as context to an LLM (OpenAI or other) with a low temperature (0.1–0.2).
- The LLM generates a focused, grounded answer that cites or uses the retrieved chunks.

3️⃣ **Local-first architecture**

- Qdrant runs locally in Docker.
- PDFs and indexes are stored locally on disk.
- Only embedding calls and LLM calls reach external APIs (unless you swap to fully local models).

---

## 🧩 Setup Guide (Windows + Conda)

> These steps are tested for local development. Adjust the commands for macOS / Linux accordingly.

### 1️⃣ Clone the repo

```bash
git clone https://github.com/<your-username>/WiiDcos.git
cd WiiDcos
```

### 2️⃣ Create & activate the environment

```bash
conda create -n willdocs python=3.10 -y
conda activate willdocs
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables

Create a `.env` file in project root and add your API keys (example):

```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
# OPTIONAL:
# QDRANT_URL=http://localhost:6333
# QDRANT_API_KEY=your_qdrant_key_if_any
```

**Important:** never commit `.env` to source control.

---

## 🐳 Run Qdrant (Docker)

```bash
cd docker
docker compose up -d
```

Open the Qdrant dashboard at: `http://localhost:6333/dashboard`

---

## ⚙️ Start the FastAPI backend

From project root:

```bash
uvicorn src.api.main:app --reload --port 8000
```

Open the API docs at: `http://127.0.0.1:8000/docs`

Routes you should expect:
- `POST /upload` — Accepts PDF uploads and starts ingestion
- `GET /query` — Query the indexed documents (or `POST /query` depending on implementation)

---

## 💬 Launch the Streamlit UI

```bash
streamlit run src/ui/app.py
```

Open the UI at: `http://localhost:8501`

Typical flow:
- Drag & drop a PDF
- Wait for "✅ Uploaded & indexed"
- Ask: "What is this PDF about?"
- Receive a short, sourced answer

---

## 🧠 Example

**Query:**

```
What is this PDF about?
```

**Answer (example):**

```
The PDF is about various research papers and studies related to speech separation using deep learning, transformer, RNN, and LSTM models.
```

---

## 🪄 Optional Improvements (Next Steps)

- **Chat History** — Persist chat sessions for better continuity in the UI.
- **Streaming Responses** — Implement streaming token-by-token output for a ChatGPT-like feel.
- **Multi-PDF Support** — Index multiple PDFs and let users choose which document(s) to query.
- **Offline Embeddings** — Replace OpenAI embeddings with local sentence-transformers to reduce API usage.
- **Full Docker Compose** — Add FastAPI + Streamlit services to `docker-compose` for single-command runs.
- **Model Flexibility** — Add a config switch to swap between OpenAI and local LLMs (e.g., Llama 2 family).

---

## ⚠️ Troubleshooting

- **Qdrant not reachable:** Ensure Docker container is running and ports are open (default `6333`).
- **Embedding errors:** Verify your `OPENAI_API_KEY` is valid and has quota. Consider local embeddings if rate-limited.
- **Slow indexing:** Chunk size and overlap configuration control speed vs. retrieval quality. Tune in `src/core/retriever.py` or LlamaIndex settings.

---

## ✅ Deployment notes

- For quick sharing, you can deploy the Streamlit app to [Streamlit Cloud] or the backend to platforms like Render or Railway.
- For production, consider: managed vector DB (Qdrant Cloud), secrets management, HTTPS, authentication, and rate-limiting.

---

## 📦 Suggested `requirements.txt` (example)

Below is a starter `requirements.txt` snippet. Pin versions to what you tested locally.

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

Adjust package versions for compatibility with your environment.

---

## 🤝 Credits

- **LlamaIndex**
- **Qdrant**
- **FastAPI**
- **Streamlit**
- **OpenAI**

---

## 🧭 TL;DR

WiiDcos RAG = Upload PDFs → Store in Qdrant → Query via LlamaIndex → Answer with OpenAI → Chat via Streamlit.

A small but complete production-style RAG stack, built with logs, tests, and lots of debugging. 💙

**Author:** Vishal Fulsundar  
🎓 *M.S. Data Science — The George Washington University*  
🔗 *LinkedIn | GitHub*

---

## 📋 Usage / Copy-paste-ready shell block (for README)

You can paste the following block directly into `README.md` if you want a ready-to-render bash-styled README section in your repository:

```bash
# 🧠 WiiDcos RAG — Chat With Your PDFs
# ... (full README contents are included in this document) ...
```


---

If you'd like, I can also:
- generate a pinned `requirements.txt` with exact versions I recommend,
- produce a `docker-compose.yml` for the full stack (FastAPI + Streamlit + Qdrant), or
- scaffold example code for `src/api/upload.py` and `src/ui/app.py`.

Tell me which of those you want next.

