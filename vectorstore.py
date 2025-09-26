from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

embedding_llm = OllamaEmbeddings(
    model="snowflake-arctic-embed:137m" 
)

# CONFIGURANDO ALGORITMO DE EMBEDDING
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
chunks = splitter.split_documents(docs) # TODO: Aguardando criação do método de carregar PDFs

def save_embeddings(chunks: str, embeddings ) -> None:
    vectorstore = FAISS.from_documents(chunks, embeddings) # Algoritmo calcula similaridade vetorial
    vectorstore.save_local("local_db") 

vectorstore = FAISS.load_local("local_db", embedding_llm)
retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.3, "k": 4}
)       