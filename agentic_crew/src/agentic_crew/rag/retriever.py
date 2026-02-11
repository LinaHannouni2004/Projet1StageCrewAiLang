import chromadb
from chromadb.utils import embedding_functions

CHROMA_PATH = "rag/vector_db"

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

class Retriever:
    def __init__(self):
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.collection = client.get_collection(
            name="enterprise_rag",
            embedding_function=embedding_function
        )

    def search(self, query, top_k=4):
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        return results["documents"][0]
