# src/core/config.py
from dotenv import load_dotenv
import os
from loguru import logger
load_dotenv()

from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding  # ✅ NEW

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

os.makedirs("./logs", exist_ok=True)
logger.add("./logs/app.log", rotation="1 MB", retention=5, enqueue=True)
logger.info("Config loaded. OPENAI key present? {}", bool(OPENAI_API_KEY))


def configure_llamaindex(temperature: float = 0.1):
    if not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY is missing.")

    # ✅ Define both LLM and embedding model
    Settings.llm = OpenAI(api_key=OPENAI_API_KEY, temperature=temperature)
    Settings.embed_model = OpenAIEmbedding(
        model="text-embedding-3-small", api_key=OPENAI_API_KEY
    )
    Settings.num_output = 512
    Settings.chunk_size = 1024


def print_keys_status():
    print(" Environment Loaded:")
    print("OPENAI_API_KEY:", "Found" if OPENAI_API_KEY else "Missing")
    print("SERPER_API_KEY:", "Found" if SERPER_API_KEY else "Missing")
    print("HF_TOKEN:", "Found" if HF_TOKEN else "Missing")


if __name__ == "__main__":
    print_keys_status()
