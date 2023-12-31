from twilio.rest import Client
from NISTaxi.sms.config import *



# Sends SMS message the the recipient phone number
# msg : Message body
# recipient_phone_number : Recipient phone number
def send_sms(msg : str, recipient_phone_number : str = '+381613099361'):
    message = client.messages.create(
        body=msg,
        from_=twilio_phone_number,
        to=recipient_phone_number
    )

    print(f"Message SID: {message.sid}")