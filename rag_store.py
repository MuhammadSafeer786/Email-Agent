from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv
load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Persistent DB on disk
vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

def add_document(doc_id, text, metadata):
    vectorstore.add_texts([text], metadatas=[metadata], ids=[doc_id])

def query(text, k=3):
    return vectorstore.similarity_search(text, k=k)
