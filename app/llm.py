from langchain_openai import AzureChatOpenAI
from config import settings


def get_llm():
    """
    Initialize and return the Azure OpenAI chat model.

    This LLM is responsible for:
    - generating grounded answers
    - reasoning over retrieved document chunks
    - producing final responses for the RAG pipeline
    """
    try:
        llm = AzureChatOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_deployment=settings.AZURE_OPENAI_CHAT_DEPLOYMENT,
            temperature=0.2,# Lower temperature reduces hallucinations and improves deterministic compliance responses
            max_tokens=512,
        )

        return llm

    except Exception as error:
        raise RuntimeError(f"Failed to initialize Azure OpenAI LLM: {str(error)}")