from dataclasses import dataclass
from typing import Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
    COLLECTION_NAME: str = "payment_docs"
    EMBEDDING_MODEL: str = "sentence-transformers/all-mpnet-base-v2"
    LLM_MODEL: str = "llama2"
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
