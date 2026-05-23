from langchain_openai import AzureOpenAIEmbeddings
from config import settings


def get_embedding_model():
    """
    Create and return the Azure OpenAI embedding model.

    This model converts text chunks into vector embeddings
    for semantic similarity search in the vector database.
    """
    return AzureOpenAIEmbeddings(
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        api_key=settings.AZURE_OPENAI_API_KEY,
        api_version=settings.AZURE_OPENAI_EMBEDDING_API_VERSION,
        azure_deployment=settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
    )