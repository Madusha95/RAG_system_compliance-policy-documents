# Compliance Document Intelligence RAG System

A Retrieval-Augmented Generation (RAG) backend service for querying AML/KYC compliance policy documents with grounded, auditable responses.

This project was developed as part of the AI Engineer Take-Home Assignment for Compliance Document Intelligence.

---

# Features

- Document ingestion pipeline
- Markdown policy parsing and chunking
- Vector embeddings with Azure OpenAI
- Persistent local vector database using ChromaDB
- Retrieval-Augmented Generation (RAG)
- Structured JSON responses
- Pydantic schema validation
- Full audit logging
- Graceful error handling
- CLI-based interface

---

# Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| LLM | Azure OpenAI `gpt-5.4`|
| Embeddings | Azure OpenAI `text-embedding-3-small` |
| Vector Database | ChromaDB |
| Framework | LangChain |
| Validation | Pydantic |
| Environment Management | python-dotenv |

---

# Project Structure

```text
project/
├── main.py                 # Application entry point and CLI command handling
├── config.py               # Environment variables and application configuration
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment variable definitions
├── audit.log               # JSON Lines audit log generated at runtime
│
├── app/
│   ├── __init__.py         # Marks app as a Python package
│   ├── audit.py            # Audit logging functionality
│   ├── chunking.py         # Document chunking logic
│   ├── embeddings.py       # Embedding model initialization
│   ├── llm.py              # LLM initialization and configuration
│   ├── loaders.py          # Markdown document loading logic
│   ├── rag.py              # Core RAG pipeline and orchestration
│   ├── schemas.py          # Pydantic response schemas and validation
│   └── vector_store.py     # ChromaDB vector store operations
│
├── chroma_db/              # Persistent Chroma vector database storage
└── policies/               # Input AML/KYC policy markdown documents
```

---

# Setup

## 1. Clone Repository

```bash
git clone https://github.com/Madusha95/RAG_system_compliance-policy-documents.git
cd RAG_system_compliance-policy-documents
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv env
env\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv env
source env/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file using `.env.example`.

Example:

```env
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-5.4

AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
AZURE_OPENAI_EMBEDDING_API_VERSION=2024-02-01

```

---

# Usage

## Ingest Documents

```bash
python main.py ingest --docs ./policies
```

This command:

- Loads markdown policy documents
- Splits documents into chunks
- Generates embeddings
- Stores vectors in ChromaDB

---

## Query Documents

```bash
python main.py query --question "What documents are required for Source of Wealth verification?" --k 3
```

### Example Output

```json
{
  "question": "What documents are required for Source of Wealth verification?",
  "answer": "Three documents are required...",
  "citations": [
    {
      "document": "02_source_of_wealth_verification_guidelines.md",
      "chunk": "..."
    }
  ],
  "model": "gpt-5.4",
  "latency_ms": 412,
  "timestamp": "2026-05-23T14:32:00Z",
  "error": null
}
```
---

# Architecture Overview

```text
Policy Documents
       ↓
Document Loader
       ↓
Chunking
       ↓
Azure OpenAI Embeddings
       ↓
Chroma Vector Store
       ↓
Similarity Retrieval
       ↓
Prompt Construction
       ↓
Azure OpenAI Chat Model
       ↓
Pydantic Schema Validation
       ↓
Structured JSON Response
       ↓
Audit Logging
```

---
# Design Decision Record

I made several non-trivial design choices to balance accuracy, maintainability, and local development simplicity. I used `gpt-5.4` deployed through Azure OpenAI as the chat model because compliance-related questions require strong reasoning, careful interpretation of policy wording, and reliable structured responses. For embeddings, I selected Azure OpenAI `text-embedding-3-small` because it provides good semantic retrieval quality while remaining cost-efficient and fast for vector search operations. LangChain was used to orchestrate the RAG pipeline because it provides clean abstractions for document loading, chunking, embeddings, vector retrieval, and prompt orchestration, which improved development speed and modularity. I used a chunk size of `800` with `250 CHUNK_OVERLAP` because AML/KYC policies frequently contain connected rules, exceptions, thresholds, and cross-referenced clauses spread across neighboring sections; the overlap helps preserve context continuity and reduces incomplete retrievals. ChromaDB was selected as the vector store because it supports persistent local storage, integrates cleanly with LangChain, and requires minimal infrastructure setup, making it suitable for local development and testing. The Retrieval-Augmented Generation (RAG) approach was used to reduce hallucinations by grounding responses in retrieved compliance documents before answer generation. The system was designed using OOP principles and modular design patterns so that responsibilities such as loading, chunking, embeddings, retrieval, schema validation, and audit logging remain separated, maintainable, reusable, and easy to extend.

# Audit Logging

Every query request is logged into `audit.log` using JSON Lines format.

Each audit entry contains:

- User question
- Final structured response
- Retrieved document chunks
- Model information
- Latency
- Timestamp
- Error details (if applicable)

This allows full reconstruction of model behavior for compliance auditing.

---

# Error Handling

The system always returns the same JSON schema even on failures.

Handled failures include:

- Empty retrieval results
- Validation errors
- API errors
- Missing document folders
- Runtime exceptions

### Example Failure Response

```json
{
  "question": "example question",
  "answer": "",
  "citations": [],
  "model": "gpt-5.4",
  "latency_ms": 100,
  "timestamp": "2026-05-23T14:32:00Z",
  "error": "empty_retrieval_result"
}
```

---

# Schema Validation

All responses are validated using Pydantic before being returned.

Validation failures are handled explicitly and converted into structured error responses instead of returning malformed output.

---

# Chunking Strategy Decision Record

I used `RecursiveCharacterTextSplitter` with:

- Chunk Size: `800`
- Chunk Overlap: `250`

This strategy was selected to preserve policy context across section boundaries while minimizing retrieval fragmentation.

Compliance policies frequently contain:

- Enumerated rules
- Threshold tables
- Exception clauses
- Cross-referenced requirements

Smaller chunks caused partial retrievals where important qualifying conditions appeared in neighboring chunks. Increasing overlap improved retrieval accuracy for nuanced and multi-document compliance questions while still maintaining efficient vector search performance.

---

# Vector Store Decision Record

ChromaDB was selected because:

- It supports persistent local storage
- It integrates cleanly with LangChain
- It requires minimal setup
- It is lightweight and suitable for local development/testing

This aligns well with the assignment requirement for a local persistent vector database without requiring external infrastructure.

---

# Security Notes

- API keys are stored only in `.env`
- `.env` is excluded from version control
- No secrets are committed to the repository

---

# Future Improvements

- Hybrid search (BM25 + vector search)
- Reranking layer
- Metadata filtering
- Streaming responses
- Async ingestion/query pipeline
- Unit and integration tests
- Docker deployment
