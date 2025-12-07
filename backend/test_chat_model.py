import os
from dotenv import load_dotenv
from rag_engine import generar_respuesta, get_rag_chain

# Force reload of env vars
load_dotenv(override=True)

print("Testing Chat Model...")
try:
    # Test 1: Check LLM model name directly
    chain = get_rag_chain()
    print(f"LLM Model Name in Chain: {chain.combine_documents_chain.llm_chain.llm.model}")
    
    # Test 2: Generate response
    query = "que es ÁMBITO DE APLICACIÓN Y PRINCIPIO"
    print(f"\nQuerying: {query}")
    response = generar_respuesta(query)
    print(f"Response: {response}")
except Exception as e:
    print(f"Error: {e}")
