
import requests
import json
import numpy as np

EMBED_MODEL = "mxbai-embed-large:latest"
LLM_MODEL = "llama3.2:latest"
VECTOR_STORE_PATH = "vector_store.json"
TOP_K = 3  # number of chunks to retrieve

def get_embedding(text):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text}
    )
    return np.array(response.json()["embedding"])

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve(query_embedding, store, top_k=TOP_K):
    scores = []
    for item in store:
        emb = np.array(item["embedding"])
        score = cosine_similarity(query_embedding, emb)
        scores.append((score, item["text"]))
    scores.sort(key=lambda x: x[0], reverse=True)
    return [text for _, text in scores[:top_k]]

def generate_answer(question, context_chunks):
    context = "\n\n---\n\n".join(context_chunks)
    prompt = f"""You are a helpful assistant. Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't have enough information to answer that."

Context:
{context}

Question: {question}

Answer:"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": LLM_MODEL, "prompt": prompt, "stream": False}
    )
    return response.json()["response"]

def main():
    print("📚 Loading vector store...")
    with open(VECTOR_STORE_PATH, "r") as f:
        store = json.load(f)
    print(f"✅ Loaded {len(store)} chunks\n")
    print("💬 RAG Chatbot ready! Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if not question:
            continue

        print("🔍 Retrieving relevant context...")
        query_embedding = get_embedding(question)
        top_chunks = retrieve(query_embedding, store)

        print("🤖 Generating answer...\n")
        answer = generate_answer(question, top_chunks)
        print(f"Assistant: {answer}\n")
        print("-" * 60 + "\n")

if __name__ == "__main__":
    main()