import time
from datetime import datetime, timezone

from langchain_core.prompts import PromptTemplate
from pydantic import ValidationError

from config import settings
from app.schemas import QueryResponse, Citation
from app.audit import AuditLogger


class RAGService:
    """
    Handles the full RAG query flow:
    - retrieve relevant chunks
    - build prompt
    - call LLM
    - validate response with Pydantic
    - write audit log
    - return structured JSON response
    """
    def __init__(self, vector_store, llm):
        self.vector_store = vector_store
        self.llm = llm
        self.audit_logger = AuditLogger()

    def answer(self, question: str, k: int):
        start_time = time.time()
        timestamp = datetime.now(timezone.utc).isoformat()
        retrieved_docs = []

        try:
            # Retrieve top-k relevant chunks from vector store
            retrieved_docs = self.vector_store.search(question, k)

            # Empty retrieval must still return the same JSON schema
            if not retrieved_docs:
                raise ValueError("No relevant chunks found.")

            # Build prompt using retrieved policy context
            context = self._build_context(retrieved_docs)
            prompt = self._build_prompt(question, context)

            answer = self.llm.invoke(prompt)
            
            response = QueryResponse(
                question=question,
                answer=str(answer.content).strip(),
                citations=[
                    Citation(
                        document=doc.metadata.get("source", "unknown"),
                        chunk=doc.page_content,
                    )
                    for doc in retrieved_docs
                ],
                model=settings.AZURE_OPENAI_CHAT_DEPLOYMENT,
                latency_ms=self._latency_ms(start_time),
                timestamp=timestamp,
            )

            # Explicit Pydantic schema validation before returning
            response = QueryResponse.model_validate(response)
        except ValidationError as error:
            # If schema validation fails, return SAME schema with error
            raise ValueError(f"response_validation_error: {str(error)}")

        except Exception as error:
            response = QueryResponse(
                question=question,
                answer="",
                citations=[],
                model=settings.AZURE_OPENAI_CHAT_DEPLOYMENT,
                latency_ms=self._latency_ms(start_time),
                timestamp=timestamp,
                error=str(error),
            )

        self.audit_logger.write({
            "question": question,
            "response": response.model_dump(),
            "retrieved_context": [
                {
                    "document": doc.metadata.get("source", "unknown"),
                    "chunk": doc.page_content,
                }
                for doc in retrieved_docs
            ],
        })

        return response

    def _build_context(self, docs):
        return "\n\n".join(
            f"Document: {doc.metadata.get('source', 'unknown')}\n"
            f"Content: {doc.page_content}"
            for doc in docs
        )

    def _build_prompt(self, question: str, context: str):
        template = PromptTemplate.from_template("""
You are a compliance document intelligence assistant.

You MUST answer using ONLY the provided context.

Rules:
- Answer ONLY the user's question.
- Be concise, accurate, and factual.
- Do NOT repeat the question.
- Do NOT repeat large parts of the context.
- Do NOT invent policies, procedures, frequencies, thresholds, or requirements.
- Do NOT generate follow-up questions.
- If multiple policy rules apply, combine them clearly.
- If the context only partially answers the question, explicitly state what is missing.
- If the answer is not contained in the context, respond exactly with:
"I don't know based on the provided documents."

For unsupported scenarios:
- Clearly state that the provided documents do not define a procedure.
- Mention any escalation or fallback guidance found in the context.
- Never fabricate compliance guidance.

Context:
{context}

Question:
{question}

Answer:
""")

        return template.format(
            context=context,
            question=question
        )

    def _latency_ms(self, start_time):
        return int((time.time() - start_time) * 1000)