import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
load_dotenv()

DATA_PATH = os.getenv("DATA_PATH")
DB_FAISS_PATH = os.getenv("DB_FAISS_PATH")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")

def create_vector_db():
    print("starting data ingestion...")
    print("loading documents from data directory...")

    loader = DirectoryLoader(
        DATA_PATH,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )
    documents = loader.load()
    print(f"loaded {len(documents)} documents from {DATA_PATH}")

    print("splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )
    text_chunks = text_splitter.split_documents(documents)
    print(f"split into {len(text_chunks)} chunks")

    print(f"loading free embedding model... {EMBEDDING_MODEL_NAME}")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"}
        )
    
    print("created embeddings...")

    print ("creating FAISS vector store...")
    vector_store = FAISS.from_documents(text_chunks, embeddings)

    print(f"saving FAISS vector store to disk at {DB_FAISS_PATH}...")
    vector_store.save_local(DB_FAISS_PATH)


if __name__ == "__main__":
    create_vector_db()