from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer


app = FastAPI()

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

index_path = "vector_store/hospital_b/faiss.index"
metadata_path = "vector_store/hospital_b/metadata.json"
index = faiss.read_index(index_path)

with open(metadata_path, "r") as f:
    metadata = json.load(f)

class SearchResult(BaseModel):
    score: float
    admission_id: str
    time: str

@app.get("/search", response_model=list[SearchResult])
def search(query: str, k: int = 5):
    query_vec = model.encode([query])
    distances, indices = index.search(np.array(query_vec).astype("float32"), k)

    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(metadata):
            meta = metadata[idx]
            results.append(SearchResult(
                score=float(distances[0][i]),
                admission_id=meta["admission_id"],
                time=meta["time"]
            ))

    return results
