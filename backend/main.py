from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import shutil
import httpx
from rag_engine import generar_respuesta, ingest_documents, DOCUMENTS_DIR

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:5173", # React default port
    "http://localhost:5174",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_CLOUD_API_TOKEN = os.getenv("WHATSAPP_CLOUD_API_TOKEN")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "whatsapp_agent_2024")

async def send_whatsapp_message(to_number: str, text: str):
    """Sends a text message via WhatsApp Cloud API."""
    if not WHATSAPP_PHONE_NUMBER_ID or not WHATSAPP_CLOUD_API_TOKEN:
        print("WhatsApp Cloud API credentials not set.")
        return

    url = f"https://graph.facebook.com/v22.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_CLOUD_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": text}
    }

    async with httpx.AsyncClient() as client:
        try:
            print(f"Sending to {url} with payload {payload}")
            response = await client.post(url, json=payload, headers=headers)
            print(f"WhatsApp Cloud API response: {response.text}")
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to send WhatsApp message: {e}")

@app.get("/")
def read_root():
    return {"message": "WhatsApp Support Agent API is running"}

from fastapi.responses import PlainTextResponse

@app.get("/webhook")
async def verify_webhook(request: Request):
    """Webhook verification challenge from WhatsApp."""
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == WHATSAPP_VERIFY_TOKEN:
            print("Webhook verified successfully!")
            return PlainTextResponse(content=challenge, status_code=200)
        else:
            raise HTTPException(status_code=403, detail="Verification failed")
    
    return {"status": "ok"}

@app.post("/webhook")
async def webhook(request: Request):
    """Endpoint to receive messages from WhatsApp Cloud API."""
    try:
        data = await request.json()
        print(f"Received webhook data: {data}")

        # Check if it's a message status update (sent, delivered, read)
        entry = data.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        
        if "statuses" in value:
            return {"status": "ignored_status_update"}

        if "messages" in value:
            message = value["messages"][0]
            from_number = message.get("from")
            message_body = message.get("text", {}).get("body", "")
            
            if not message_body:
                print("No text body in message")
                return {"status": "no_text_body"}

            print(f"Processing message from {from_number}: {message_body}")
            
            # Generate response using RAG
            response_text = generar_respuesta(message_body)
            print(f"Generated response: {response_text}")
            
            # Send response back to WhatsApp
            await send_whatsapp_message(from_number, response_text)
            
            return {"status": "processed", "response": response_text}
            
        return {"status": "no_messages_found"}

    except Exception as e:
        print(f"Error processing webhook: {e}")
        # Always return 200 to WhatsApp to prevent retries
        return {"status": "error", "detail": str(e)}

@app.post("/api/chat")
async def chat(request: Request):
    """Endpoint for the Dashboard to test the bot."""
    data = await request.json()
    question = data.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")
    
    response = generar_respuesta(question)
    return {"response": response}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Endpoint to upload PDF/TXT files."""
    try:
        file_path = os.path.join(DOCUMENTS_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Trigger ingestion after upload
        ingest_documents()
        
        return {"message": f"File {file.filename} uploaded and ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents")
def list_documents():
    """List uploaded documents."""
    if not os.path.exists(DOCUMENTS_DIR):
        return []
    return [f for f in os.listdir(DOCUMENTS_DIR) if f.endswith(('.pdf', '.txt'))]

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
