import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Centralized application configuration.

    This class stores:
    - vector database settings
    - Azure OpenAI configuration
    - chunking configuration
    - retrieval configuration
    """

    # Vector DB
    DB_PATH = "./chroma_db"
    COLLECTION_NAME = "compliance_policies"

    # Azure OpenAI
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

    # Deployments
    AZURE_OPENAI_CHAT_DEPLOYMENT = os.getenv(
        "AZURE_OPENAI_CHAT_DEPLOYMENT"
    )

    AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv(
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT"
    )

    AZURE_OPENAI_EMBEDDING_API_VERSION = os.getenv(
        "AZURE_OPENAI_EMBEDDING_API_VERSION"
    )

    # Chunking
    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 250

    # Retrieval
    DEFAULT_K = 3


settings = Settings()