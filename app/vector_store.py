from langchain_chroma import Chroma
from config import settings


class VectorStore:
    """
    Handles vector database operations using ChromaDB.

    Responsibilities:
    - store embedded document chunks
    - load persistent vector database
    - perform semantic similarity search
    """
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model

    def save(self, documents):
        return Chroma.from_documents(
            documents=documents,
            embedding=self.embedding_model,
            persist_directory=settings.DB_PATH,
            collection_name=settings.COLLECTION_NAME,
        )

    def load(self):
        return Chroma(
            persist_directory=settings.DB_PATH,
            embedding_function=self.embedding_model,
            collection_name=settings.COLLECTION_NAME,
        )

    def search(self, question: str, k: int):
        db = self.load()
        return db.similarity_search(question, k=k)