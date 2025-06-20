from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

from config import api_key

def create_retriever(documents, persist_path="faiss_index"):
    docs = [Document(page_content=d["content"], metadata={"source": d["source"]}) for d in documents]
    embedding = OpenAIEmbeddings(
            api_key=api_key,
            model="text-embedding-3-large",
            )
    vectorstore = FAISS.from_documents(docs, embedding)
    return vectorstore.as_retriever()
