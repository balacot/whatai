import os
from typing import List
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# Configuration
DOCUMENTS_DIR = "../documentos"
CHROMA_DB_DIR = "./chroma_db"

def load_documents(directory: str) -> List:
    documents = []
    if not os.path.exists(directory):
        os.makedirs(directory)
        return []

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
        elif filename.endswith(".txt"):
            loader = TextLoader(file_path)
            documents.extend(loader.load())
    return documents

def ingest_documents():
    """Reads documents, splits them, and stores embeddings in ChromaDB."""
    print("Loading documents...")
    docs = load_documents(DOCUMENTS_DIR)
    if not docs:
        print("No documents found to ingest.")
        return

    print(f"Found {len(docs)} pages/documents.")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    
    print(f"Splitting into {len(splits)} chunks...")

    # Use Local Embeddings (HuggingFace)
    print("Initializing Local Embeddings (this may take a while on first run)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Create or update vector store
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings, 
        persist_directory=CHROMA_DB_DIR
    )
    vectorstore.persist()
    print("Ingestion complete. Vector store persisted.")

def get_rag_chain():
    """Initializes and returns the RAG chain."""
    # Use Local Embeddings (HuggingFace)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)
    
    print("Initializing LLM with model: gemini-flash-latest")
    llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", google_api_key=GOOGLE_API_KEY, temperature=0.2)
    
    template = """Usa SOLO el siguiente contexto para responder la pregunta del usuario en WhatsApp. 
    Si no encuentras la respuesta en el contexto, di que no tienes esa información.
    
    Contexto:
    {context}
    
    Pregunta: {question}
    
    Respuesta:"""
    
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 6}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    
    return qa_chain

def generar_respuesta(pregunta_usuario: str) -> str:
    """Generates a response for a given user question."""
    try:
        qa_chain = get_rag_chain()
        result = qa_chain({"query": pregunta_usuario})
        
        # DEBUG: Print retrieved documents to console
        source_docs = result.get('source_documents', [])
        print(f"\n--- DEBUG: Retrieved {len(source_docs)} chunks for query: '{pregunta_usuario}' ---")
        for i, doc in enumerate(source_docs):
            print(f"[Chunk {i+1}] Source: {doc.metadata.get('source', 'unknown')}")
            print(f"Content: {doc.page_content[:200]}...\n")
        print("------------------------------------------------------------------\n")

        return result["result"]
    except Exception as e:
        return f"Error generando respuesta: {str(e)}"

if __name__ == "__main__":
    # For testing purposes
    # ingest_documents() # Uncomment to ingest on run
    # print(generar_respuesta("Hola, ¿qué documentos tienes?"))
    pass
