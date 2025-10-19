import streamlit as st
import requests
import os

# ----------- CONFIG -----------
FASTAPI_URL = "http://127.0.0.1:8000"   # make sure FastAPI server is running
UPLOAD_ENDPOINT = f"{FASTAPI_URL}/upload/"
QUERY_ENDPOINT = f"{FASTAPI_URL}/query/"

st.set_page_config(page_title="📚 WiiDcos RAG", layout="centered")
st.title("📚 WiiDcos RAG App – Chat with Your PDFs")

# ----------- FILE UPLOAD -----------
st.header("1️⃣  Upload a PDF to index")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Uploading and ingesting..."):
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        res = requests.post(UPLOAD_ENDPOINT, files=files)
    if res.status_code == 200:
        st.success(f"✅ Uploaded & indexed: {uploaded_file.name}")
    else:
        st.error(f"❌ Upload failed: {res.text}")

st.divider()

# ----------- QUERY SECTION -----------
st.header("2️⃣  Ask a Question about the PDFs")

query = st.text_input("Enter your question:")
if st.button("Ask"):
    if not query.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Thinking..."):
            res = requests.get(QUERY_ENDPOINT, params={"q": query})
        if res.status_code == 200:
            answer = res.json().get("answer", "No answer.")
            st.markdown(f"### 💬 Answer:\n{answer}")
        else:
            st.error(f"❌ Query failed: {res.text}")

st.divider()
st.caption("Built with 🧠 LlamaIndex + Qdrant + FastAPI + Streamlit")
