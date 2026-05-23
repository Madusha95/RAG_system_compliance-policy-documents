from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import settings


class DocumentChunker:
    def split(self, documents):
        """
        Split loaded documents into smaller overlapping chunks.

        Parameters:
            documents (list): List of LangChain document objects.

        Returns:
            list: List of chunked document objects.
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
        )

        return splitter.split_documents(documents)