
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
import os

def build_simple_index(data_dir: str = "./Data", persist_dir: str = "./storage/index"):
    print(" Building simple index...")
    os.makedirs(persist_dir, exist_ok=True)

    documents = SimpleDirectoryReader(data_dir).load_data()
    index = VectorStoreIndex.from_documents(documents)

    index.storage_context.persist(persist_dir)
    print(f" Index created and saved to {persist_dir}")

if __name__ == "__main__":
    build_simple_index()
