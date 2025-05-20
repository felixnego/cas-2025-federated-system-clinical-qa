import psycopg2
import faiss
import os
import pandas as pd
from models.embedder import Embedder


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "mimic_a",
    "user": "admin",
    "password": "admin"
}

def extract_notes():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT admission_id, time, text
        FROM notes
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    docs = []
    meta = []

    for admission_id, time, text in results:
        docs.append(text)
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
    embedder = Embedder("sentence-transformers/all-MiniLM-L6-v2")
    vectors = embedder.embed(docs)
    
    os.makedirs("./vector_store", exist_ok=True)
    save_vector_store(vectors, meta, "./vector_store/faiss.index", "./vector_store/metadata.json")
    print(f"✅ Embedded {len(docs)} documents and saved FAISS index + metadata.")


if __name__ == "__main__":
    main()
