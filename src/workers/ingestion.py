from inngest import Inngest
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from src.core.qdrant_store import configure_qdrant
from src.core.config import configure_llamaindex

inngest = Inngest(app_id="wiidcos")

@inngest.create_function(trigger=inngest.trigger.event("doc/ingest.requested"))
def ingest_document(event):
    data = event["data"]
    file_path = data["path"]
    file_name = data["filename"]

    configure_llamaindex(temperature=0.1)
    configure_qdrant()

    print(f" Ingesting {file_name} ...")
    docs = SimpleDirectoryReader(input_files=[file_path]).load_data()
    index = VectorStoreIndex.from_documents(docs)
    print(f" Ingested {file_name} successfully.")

    return {"status": "completed", "filename": file_name}
