import psycopg2
import faiss
import os
import numpy as np
import pandas as pd
from models.embedder import Embedder


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "umcdb_b",
    "user": "admin",
    "password": "admin"
}

def extract_notes():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT admission_id, time, note FROM freetextitems")
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    docs = []
    meta = []

    for admission_id, time, note in results:
        docs.append(note)
        meta.append({"admission_id": admission_id, "time": str(time)})

    return docs, meta

def save_vector_store(embeddings, metadata, index_path, meta_path):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, index_path)
    pd.DataFrame(metadata).to_json(meta_path, orient="records", indent=2)


def main():
    docs, meta = extract_notes()
    embedder = Embedder()
    vectors = embedder.embed(docs)

    os.makedirs("vector_store/hospital_b", exist_ok=True)
    save_vector_store(vectors, meta, "vector_store/hospital_b/faiss.index", "vector_store/hospital_b/metadata.json")
    print(f"✅ Embedded {len(docs)} notes for Hospital B.")


if __name__ == "__main__":
    main()
