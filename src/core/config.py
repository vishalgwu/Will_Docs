# src/core/config.py
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def print_keys_status():
    print(" Environment Loaded:")
    print("OPENAI_API_KEY:", "Found" if OPENAI_API_KEY else "Missing")
    print("SERPER_API_KEY:", "Found" if SERPER_API_KEY else "Missing")

if __name__ == "__main__":
    print_keys_status()
