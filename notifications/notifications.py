from fastapi import FastAPI, HTTPException
from twilio.rest import Client
import os
import openai

# Initialize FastAPI
app = FastAPI()

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# OpenAI configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

@app.post("/webhook")
async def receive_webhook(data: dict):
    """
    Receive webhook notifications from the monitoring service and process them with OpenAI.
    """
    try:
        # Extract relevant information from the webhook data
        phone_number = data.get('phone_number')
        event_details = data.get('event_details')

        if not phone_number or not event_details:
            raise ValueError("Missing required fields in webhook data")

        # Use OpenAI to generate a response based on the event details
        response = openai.Completion.create(
            engine="#",
            prompt=f"Based on the following event details: {event_details}, what should the response be?",
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Extract the generated message from the response
        message = response.choices[0].text.strip()

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
