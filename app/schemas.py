from typing import List, Optional
from pydantic import BaseModel


class Citation(BaseModel):
    """
    Represents a citation returned from retrieved policy documents.
    """
    document: str
    chunk: str


class QueryResponse(BaseModel):
    """
    Standardized response schema for all query responses.
    """
    question: str
    answer: str
    citations: List[Citation]
    model: str
    latency_ms: int
    timestamp: str
    error: Optional[str] = None