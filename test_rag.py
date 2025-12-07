import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from rag_engine import ingest_documents, generar_respuesta

def test_rag():
    print("--- Testing RAG Engine ---")
    
    # 1. Ingest documents
    print("\n1. Ingesting documents...")
    try:
        ingest_documents()
    except Exception as e:
        print(f"Error during ingestion: {e}")
        return

    # 2. Ask a question
    question = "Cuál es el plazo de devolución?"
    print(f"\n2. Asking question: '{question}'")
    
    try:
        answer = generar_respuesta(question)
        print(f"\nAnswer: {answer}")
    except Exception as e:
        print(f"Error generating answer: {e}")

if __name__ == "__main__":
    test_rag()
