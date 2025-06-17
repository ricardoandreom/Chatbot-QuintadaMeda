from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document

def create_retriever(documents, persist_path="faiss_index"):
    docs = [Document(page_content=d["content"], metadata={"source": d["source"]}) for d in documents]
    embedding = OpenAIEmbeddings(
            model="text-embedding-3-large",
            )
    vectorstore = FAISS.from_documents(docs, embedding)
    return vectorstore.as_retriever()
