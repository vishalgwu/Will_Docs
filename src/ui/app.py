# src/ui/app.py
import streamlit as st
import requests

FASTAPI_URL = "http://127.0.0.1:8000"
UPLOAD_ENDPOINT = f"{FASTAPI_URL}/upload/"
QUERY_ENDPOINT = f"{FASTAPI_URL}/query/"

st.set_page_config(page_title="📚 WiiDcos RAG", layout="centered")
st.title("📚 WiiDcos RAG App – Chat with Your PDFs")

# ---- session state ----
if "docs" not in st.session_state:
    st.session_state.docs = []  # [{"filename": "...", "doc_id": "..."}]
if "selected_filename" not in st.session_state:
    st.session_state.selected_filename = None

colA, colB = st.columns([1,1])
with colA:
    if st.button("🧹 Clear session (reset)"):
        st.session_state.clear()
    try:
        st.rerun()  # ✅ new stable API
    except Exception:
        # fallback for older Streamlit versions
        import streamlit.runtime.scriptrunner as scriptrunner
        scriptrunner.RerunException(scriptrunner.RerunData(None))

with colB:
    st.caption("If you deleted/changed the collection, clear to avoid stale IDs.")

st.header("1️⃣ Upload a PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
if uploaded_file is not None:
    with st.spinner("Uploading and ingesting..."):
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        res = requests.post(UPLOAD_ENDPOINT, files=files, timeout=120)
    if res.status_code == 200:
        data = res.json()
        filename = data.get("filename", uploaded_file.name)
        st.success(f"✅ Uploaded & indexed: {filename}")
        st.session_state.docs.append({"filename": filename, "doc_id": data.get("doc_id")})
        st.session_state.selected_filename = filename
    else:
        st.error(f"❌ Upload failed: {res.text}")

st.divider()

st.header("2️⃣ Select a document to query")
use_all_docs = st.toggle("🔎 Search all documents (ignore selection)", value=False)

if st.session_state.docs:
    filenames = [d["filename"] for d in st.session_state.docs]
    default_idx = filenames.index(st.session_state.selected_filename) if st.session_state.selected_filename in filenames else 0
    chosen = st.selectbox("Choose document:", filenames, index=default_idx)
    st.session_state.selected_filename = chosen
else:
    st.info("Upload at least one PDF to start querying.")

st.header("3️⃣ Ask a Question")
query = st.text_input("Your question:")
if st.button("Ask"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        params = {"q": query}
        if not use_all_docs and st.session_state.selected_filename:
            params["source"] = st.session_state.selected_filename  # ✅ filter by filename

        with st.spinner("Thinking..."):
            try:
                res = requests.get(QUERY_ENDPOINT, params=params, timeout=120)
                if res.status_code == 200:
                    data = res.json()
                    answer = data.get("answer", "")
                    if not answer or not answer.strip():
                        st.warning("⚠️ Empty response. Try enabling 'Search all documents', or re-upload to refresh metadata.")
                    else:
                        st.markdown("### 💬 Answer")
                        st.write(answer)
                    with st.expander("🔧 Debug (response)"):
                        st.write({"params_sent": params, "raw_json": data})
                else:
                    st.error(f"❌ Query failed: {res.status_code} | {res.text}")
            except Exception as e:
                st.error(f"❌ Request error: {e}")

st.divider()
st.caption("Built with 🧠 LlamaIndex + Qdrant + FastAPI + Streamlit")
