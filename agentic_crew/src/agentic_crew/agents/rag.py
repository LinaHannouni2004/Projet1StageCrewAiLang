from rag.retriever import Retriever

class RAGAgent:
    def __init__(self):
        self.retriever = Retriever()

    def retrieve(self, query):
        results = self.retriever.search(query)
        return "\n\n".join(results)
    
    def run(self, query):
        context = self.retrieve(query)
        if not context.strip():
            return "No relevant information found in documents."
        return context