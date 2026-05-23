import argparse
import json

from config import settings
from app.loaders import PolicyLoader
from app.chunking import DocumentChunker
from app.embeddings import get_embedding_model
from app.llm import get_llm
from app.vector_store import VectorStore
from app.rag import RAGService


def ingest(docs_path: str):
    """
    Run the document ingestion pipeline.

    This command:
    - loads markdown policy documents
    - splits them into chunks
    - generates embeddings
    - saves them into ChromaDB
    """
    embedding_model = get_embedding_model()

    # Initialize pipeline components
    loader = PolicyLoader()
    chunker = DocumentChunker()
    vector_store = VectorStore(embedding_model)

    # Load and chunk documents
    documents = loader.load(docs_path)
    chunks = chunker.split(documents)

    # Save chunks into vector database
    vector_store.save(chunks)

    # Print JSON output for CLI consistency
    print(json.dumps({
        "status": "success",
        "chunks_ingested": len(chunks)
    }))


def query(question: str, k: int):
    """
    Run the RAG query pipeline.

    This command:
    - loads embeddings
    - loads the LLM
    - retrieves top-k relevant chunks
    - generates an answer
    - prints a validated JSON response
    """
    embedding_model = get_embedding_model()
    llm = get_llm()

    # Initialize vector store and RAG service
    vector_store = VectorStore(embedding_model)
    rag_service = RAGService(vector_store, llm)

    # Generate structured response
    response = rag_service.answer(question, k)

    # Query command must print only valid JSON to stdout
    print(response.model_dump_json(indent=2))


def main():
    """
    CLI entry point.

    Supported commands:
    - ingest --docs <folder_path>
    - query --question "<question>" [--k <number>]
    """
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    # Ingest command
    ingest_parser = subparsers.add_parser("ingest")
    ingest_parser.add_argument("--docs", required=True)

    # Query command
    query_parser = subparsers.add_parser("query")
    query_parser.add_argument("--question", required=True)
    query_parser.add_argument("--k", type=int, default=settings.DEFAULT_K)

    args = parser.parse_args()

    # Route command to correct function
    if args.command == "ingest":
        ingest(args.docs)

    elif args.command == "query":
        query(args.question, args.k)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()