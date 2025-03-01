from twilio.rest import Client
from config import TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE

def connect_call(from_number, to_number):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    call = client.calls.create(
        to=to_number,
        from_=TWILIO_PHONE,
        url="http://your-server/connect_message"  # Add later
    )
    return call.sid