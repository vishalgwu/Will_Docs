import streamlit as st, requests

st.set_page_config(page_title="WiiDcos RAG", layout="centered")
st.title("WiiDcos RAG App – Chat with Your PDFs")

st.header("Upload PDFs")
files = st.file_uploader("Choose PDF files", type=["pdf"], accept_multiple_files=True)
if files:
    for f in files:
        r = requests.post("http://localhost:8000/upload",
                          files={"file": (f.name, f, "application/pdf")})
        st.success(r.json()["message"])

st.header(" Ask a Question")
query = st.text_input("Your question:")
if st.button("Ask"):
    r = requests.post("http://localhost:8000/query", json={"query": query})
    st.write(r.json())
