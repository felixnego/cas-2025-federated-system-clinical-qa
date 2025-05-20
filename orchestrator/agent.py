import httpx


HOSPITAL_ENDPOINTS = {
    "hospital_a": "http://localhost:8001/search",
    "hospital_b": "http://localhost:8002/search",
    "hospital_c": "http://localhost:8003/search",
}

async def query_hospital(client, name, query, k):
    try:
        response = await client.get(HOSPITAL_ENDPOINTS[name], params={"query": query, "k": k})
        response.raise_for_status()
        results = response.json()
        for r in results:
            r["source"] = name
        return results
    except Exception as e:
        print(f"[ERROR] {name}: {e}")
        return []

async def aggregate_results(query: str, k: int = 5):
    async with httpx.AsyncClient() as client:
        from asyncio import gather
        responses = await gather(*[
            query_hospital(client, name, query, k)
            for name in HOSPITAL_ENDPOINTS
        ])
    
    # Flatten and sort by score (lower is better in FAISS)
    flat_results = [r for hospital_results in responses for r in hospital_results]
    sorted_results = sorted(flat_results, key=lambda r: r["score"])
    return sorted_results[:k]
