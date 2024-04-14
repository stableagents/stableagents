from fastapi import FastAPI, HTTPException
from twilio.rest import Client
import os

# Initialize FastAPI
app = FastAPI()

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.post("/webhook")
async def receive_webhook(data: dict):
    """
    Receive webhook notifications from the monitoring service.
    """
    try:
        # Extract relevant information from the webhook data
        phone_number = data.get('phone_number')
        message = data.get('message')

        if not phone_number or not message:
            raise ValueError("Missing required fields in webhook data")

        # Send SMS notification using Twilio
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return {"status": "success", "message_id": message.sid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
