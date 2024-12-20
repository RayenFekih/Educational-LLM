from dataclasses import dataclass

from langchain.embeddings import HuggingFaceEmbeddings
from langchain_core.vectorstores.base import VectorStore
from langchain_groq import ChatGroq

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)
LLM_model = ChatGroq(model_name="llama-3.1-70b-versatile")


@dataclass
class GlobalStore:
    value: VectorStore = None


vectorstore = GlobalStore()
