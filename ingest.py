import pdfplumber
import requests
import json
import numpy as np

PDF_PATH = "Hyderabad_Full_Day_Tour.pdf"
EMBED_MODEL = "mxbai-embed-large:latest"
VECTOR_STORE_PATH = "vector_store.json"
CHUNK_SIZE = 300      # words per chunk
CHUNK_OVERLAP = 50    # words overlap between chunks

def extract_text(pdf_path):
    text = ""
    with pdfplumber.open("C:/Users/VarunKumarKarnati/Desktop/L1/Hyderabad.pdf") as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def get_embedding(text):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text}
    )
    return response.json()["embedding"]
#def get_embedding(text):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=60  # ← this was missing
    )
    data = response.json()
    return data["embedding"]

def ingest():
    print("📄 Extracting text from PDF...")
    text = extract_text(PDF_PATH)
    print(f"✅ Extracted {len(text.split())} words")

    print("✂️  Chunking text...")
    chunks = chunk_text(text)
    print(f"✅ Created {len(chunks)} chunks")

    print("🔢 Generating embeddings (this may take a moment)...")
    store = []
    for i, chunk in enumerate(chunks):
        print(f"   Embedding chunk {i+1}/{len(chunks)}...")
        embedding = get_embedding(chunk)
        store.append({"id": i, "text": chunk, "embedding": embedding})

    with open(VECTOR_STORE_PATH, "w") as f:
        json.dump(store, f)

    print(f"\n✅ Done! Vector store saved to '{VECTOR_STORE_PATH}'")
    print(f"   Total chunks stored: {len(store)}")

if __name__ == "__main__":
    ingest()