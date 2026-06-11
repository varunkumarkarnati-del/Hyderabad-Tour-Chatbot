# Hyderabad-Tour-Chatbot
# 📄 Local RAG System with Ollama

A fully local Retrieval-Augmented Generation (RAG) system that lets you chat with any PDF file using open-source models — no internet, no API keys, no cloud.

Built with **Ollama**, **mxbai-embed-large** for embeddings, **llama3.2** for generation, and a lightweight JSON file as the vector store.

---

## 🛠️ Tech Stack

| Component       | Tool                       |
|-----------------|----------------------------|
| Embedding Model | mxbai-embed-large:latest   |
| LLM             | llama3.2:latest            |
| Vector Store    | JSON file (local)          |
| PDF Extraction  | pdfplumber                 |
| Runtime         | Ollama (local)             |

---

## 📁 Project Structure

    rag_project/
    ├── your_file.pdf          <- Your input PDF
    ├── ingest.py              <- Extract, chunk, embed and save to vector store
    ├── query.py               <- Ask questions against your PDF
    ├── vector_store.json      <- Auto-generated after running ingest.py
    └── README.md

---

## ⚙️ Prerequisites

### 1. Python 3.8+
Download from https://www.python.org/downloads/

> Make sure to check "Add Python to PATH" during installation on Windows.

### 2. Ollama
Download from https://ollama.com/download and install it.

Then pull the required models:

    ollama pull mxbai-embed-large:latest
    ollama pull llama3.2:latest

### 3. Python Dependencies

    pip install pdfplumber numpy requests

---

## 🚀 How to Run

### Step 1 — Add your PDF
Place your PDF file in the project folder and update the PDF_PATH variable in ingest.py:

    PDF_PATH = "your_file.pdf"

### Step 2 — Ingest the PDF (run once)

    python ingest.py

This will:
- Extract text from the PDF
- Split it into overlapping chunks (300 words, 50 word overlap)
- Generate embeddings for each chunk using mxbai-embed-large
- Save all chunks + embeddings to vector_store.json

### Step 3 — Ask Questions

    python query.py

Type your questions and get answers grounded in your PDF content. Type `exit` to quit.

---

## 💬 Example Session

    Loaded 36 chunks

    RAG Chatbot ready! Type 'exit' to quit.

    You: What time does the tour start?
    Retrieving relevant context...
    Generating answer...

    Assistant: The tour departs at 08:30am after breakfast.

    You: What is included in the tour price?
    Retrieving relevant context...
    Generating answer...

    Assistant: The tour price of INR 5800 per person includes an AC tempo
    traveler, English speaking guide, monument entrance fees, Biryani lunch,
    snacks during the tour, and all applicable taxes.

---

## ⚙️ How It Works

    PDF
     └─► Extract text (pdfplumber)
          └─► Split into chunks
               └─► Embed each chunk (mxbai-embed-large via Ollama)
                    └─► Save to vector_store.json
                                   │
                         ┌─────────┘
    Question             │
     └─► Embed question──┘
          └─► Cosine similarity search → Top 3 chunks
               └─► Send chunks + question to llama3.2
                    └─► Grounded answer

---

## ⚠️ Important Notes

- Ollama must be running in the background before you run either script.
  If it is not running, start it with: `ollama serve`
- Run ingest.py only once per PDF. Re-run it only if you change the PDF.
- vector_store.json can be large depending on your PDF size — add it to .gitignore if needed.
- On Windows, if you get a script execution error, run this in PowerShell:
  `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## 📦 Dependencies

    pdfplumber
    numpy
    requests

All models run locally via Ollama. No external API calls are made.

---

## 🙌 Acknowledgements

- [Ollama](https://ollama.com) — local LLM runtime
- [mxbai-embed-large](https://ollama.com/library/mxbai-embed-large) — embedding model by MixedBread AI
- [llama3.2](https://ollama.com/library/llama3.2) — LLM by Meta
- [pdfplumber](https://github.com/jsvine/pdfplumber) — PDF text extraction
