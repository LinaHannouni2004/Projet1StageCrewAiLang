from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from agents.rag import RAGAgent


class RAGToolInput(BaseModel):
    query: str = Field(..., description="User query for RAG search")


class RAGTool(BaseTool):
    name: str = "Enterprise RAG Search"
    description: str = "Retrieve knowledge from internal documents using RAG."
    args_schema: Type[BaseModel] = RAGToolInput

    def _run(self, query: str) -> str:
        rag = RAGAgent()
        return rag.run(query)
