from ollama import chat

def generate_summary(query: str, documents: list) -> str:
    context = "\n\n".join(
        f"[{doc['source']}] {doc.get('text', f'entry at {doc.get('time')}')}" for doc in documents
    )
    
    prompt = f"""
You are a clinical assistant. A user has asked: "{query}"

Here is relevant information retrieved from different hospitals:

{context}

Based on this, provide a concise and clinically accurate answer:
"""
    response = chat(model='llama3', messages=[
        {"role": "user", "content": prompt}
    ])

    return response['message']['content'].strip()
