

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
import os



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "documents")
CHROMA_PATH = "rag/vector_db"

embedding_functions = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def ingest_documents():

  client = chromadb.PersistentClient(path=CHROMA_PATH)

  collection = client.get_or_create_collection(name="documents", embedding_function=embedding_functions)

  splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)

  for file in os.listdir(DATA_PATH):
    if file.endswith(".pdf"):
      loader = PyPDFLoader(os.path.join(DATA_PATH, file))
      pages = loader.load()
      chunks = splitter.split_documents(pages) 
      
      documents = [chunk.page_content for chunk in chunks]
      metadatas = [{"source": file} for _ in chunks]
      ids = [f"{file}_{i}" for i in range(len(chunks))]

      collection.add(documents=documents, metadatas=metadatas, ids=ids)

      print("fichier ingéré")

if __name__ == "__main__":
    ingest_documents()


