import json
import math
import os
from uuid import uuid4

class MemoryStore:
    def __init__(self, embedding_engine, persist_path="./.ai_memory/memory.json"):
        self.encoder = embedding_engine
        self.path = persist_path
        os.makedirs(os.path.dirname(persist_path), exist_ok=True)
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                return json.load(f)
        return {"entries": []}

    def _save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add(self, text, metadata=None, embedding=None):
        if embedding is None:
            embedding = self.encoder.encode([text])[0]
        entry = {
            "id": str(uuid4()),
            "text": text,
            "embedding": embedding,
            "metadata": metadata or {}
        }
        self.data["entries"].append(entry)
        self._save()
        return entry["id"]

    def search(self, query_text, k=5):
        query_vec = self.encoder.encode([query_text])[0]
        results = []
        for entry in self.data["entries"]:
            sim = self._cosine_sim(query_vec, entry["embedding"])
            results.append((sim, entry))
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:k]]

    def _cosine_sim(self, a, b):
        dot = sum(x*y for x,y in zip(a,b))
        norm_a = math.sqrt(sum(x*x for x in a))
        norm_b = math.sqrt(sum(x*x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def get_all(self):
        return self.data["entries"]