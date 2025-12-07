import asyncio
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_CLOUD_API_TOKEN = os.getenv("WHATSAPP_CLOUD_API_TOKEN")

async def send_test_message(to_number: str):
    print(f"Sending message to {to_number}...")
    
    url = f"https://graph.facebook.com/v22.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_CLOUD_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": "Hola! Esta es una prueba desde tu Agente de Soporte con IA."}
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Failed to send: {e}")

if __name__ == "__main__":
    # Replace with the number you want to test (must include country code)
    # User requested: 3017800356. Assuming Colombia (+57) based on typical format, 
    # but user should confirm. I will try adding 57.
    target_number = "573017800356" 
    asyncio.run(send_test_message(target_number))
