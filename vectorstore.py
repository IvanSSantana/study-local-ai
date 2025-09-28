from langchain_chroma import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
import os

# Cria a pasta que armazenará o vectorstore
DB_PATH = "local_vectorstore"
if not os.path.exists(DB_PATH):
    os.makedirs(DB_PATH)

embedding_llm = OllamaEmbeddings(
    model="snowflake-arctic-embed:33m" 
) # type: ignore

def save_embeddings(doc: List[Document]) -> None:
    # CONFIGURANDO ALGORITMO DE EMBEDDING
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=80) 
    chunks = splitter.split_documents(doc)

    # Cria o banco Chroma local
    vectorstore = Chroma.from_documents(
        chunks,
        embedding_llm,
        persist_directory=DB_PATH
    )

    print("INFO - Arquivo salvo na IA com sucesso!")

def load_vectorstore():
    # Carrega o banco Chroma local
    vectorstore = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding_llm
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.4, "k": 5}
    )

    return (vectorstore, retriever)