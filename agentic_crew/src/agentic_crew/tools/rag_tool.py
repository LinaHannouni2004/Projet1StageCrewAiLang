from crewai.tools import BaseTool
from agents.rag import RAGAgent

class RAGTool(BaseTool):
    name = "Enterprise RAG Search"
    description = "Retrieve knowledge from internal documents using RAG."

    def _run(self, query: str):
        rag = RAGAgent()
        return rag.run(query)
