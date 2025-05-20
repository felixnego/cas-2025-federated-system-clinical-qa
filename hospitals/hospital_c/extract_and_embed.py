import psycopg2
import faiss
import os
import numpy as np
import pandas as pd
from models.embedder import Embedder


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "hirid_c",
    "user": "admin",
    "password": "admin"
}

def synthesize_notes():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Synthesize from observations
    cursor.execute("""
        SELECT patient_id, timestamp, variable_name, value
        FROM observations
        ORDER BY patient_id, timestamp
    """)
    obs_results = cursor.fetchall()

    # Synthesize from pharma
    cursor.execute("""
        SELECT patient_id, timestamp, medication, dose, unit
        FROM pharma
        ORDER BY patient_id, timestamp
    """)
    pharma_results = cursor.fetchall()

    conn.close()

    notes = []
    meta = []

    for patient_id, ts, var, val in obs_results:
        notes.append(f"Patient {patient_id} had {var} of {val} at {ts}.")
        meta.append({"patient_id": patient_id, "time": str(ts)})

    for patient_id, ts, med, dose, unit in pharma_results:
        notes.append(f"Patient {patient_id} received {med} at {dose} {unit} on {ts}.")
        meta.append({"patient_id": patient_id, "time": str(ts)})

    return notes, meta

def save_vector_store(embeddings, metadata, index_path, meta_path):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, index_path)
    pd.DataFrame(metadata).to_json(meta_path, orient="records", indent=2)


def main():
    docs, meta = synthesize_notes()
    embedder = Embedder()
    vectors = embedder.embed(docs)

    os.makedirs("vector_store/hospital_c", exist_ok=True)
    save_vector_store(vectors, meta, "vector_store/hospital_c/faiss.index", "vector_store/hospital_c/metadata.json")
    print(f"✅ Synthesized and embedded {len(docs)} notes for Hospital C.")


if __name__ == "__main__":
    main()
