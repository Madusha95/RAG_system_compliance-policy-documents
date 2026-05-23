from pathlib import Path
from langchain_community.document_loaders import TextLoader


class PolicyLoader:
    """
    Loads markdown policy documents from the provided folder.

    This component is responsible for:
    - validating the documents directory
    - reading markdown files
    - attaching source metadata to each document
    """
    def load(self, docs_path: str):
        folder = Path(docs_path)

        if not folder.exists():
            raise FileNotFoundError(f"Documents folder not found: {docs_path}")

        documents = []

        for file_path in folder.glob("*.md"):
            loader = TextLoader(str(file_path), encoding="utf-8")
            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = file_path.name

            documents.extend(docs)

        if not documents:
            raise ValueError("No markdown documents found.")

        return documents