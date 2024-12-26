from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, Record
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import numpy as np
from ..config import Config

class VectorStore:
    def __init__(self, config: Config):
        self.config = config
        self.client = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)
        self.embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)

        # Initialize collection if it doesn't exist
        self._init_collection()

    def _init_collection(self):
        collections = self.client.get_collections().collections
        if not any(c.name == self.config.COLLECTION_NAME for c in collections):
            self.client.create_collection(
                collection_name=self.config.COLLECTION_NAME,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE)
            )

    def add_documents(self, documents: List[Dict[str, Any]]):
        embeddings = self.embedding_model.encode([doc["content"] for doc in documents])

        records = [
            Record(
                id=idx,
                vector=embedding.tolist(),
                payload=doc
            ) for idx, (doc, embedding) in enumerate(zip(documents, embeddings))
        ]

        self.client.upload_records(
            collection_name=self.config.COLLECTION_NAME,
            records=records
        )

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        query_embedding = self.embedding_model.encode(query)
        results = self.client.search(
            collection_name=self.config.COLLECTION_NAME,
            query_vector=query_embedding.tolist(),
            limit=limit
        )
        return [hit.payload for hit in results]
