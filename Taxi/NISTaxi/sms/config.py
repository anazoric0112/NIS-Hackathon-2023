from twilio.rest import Client

account_sid = 'ACd92628dd0666c95f82391502d224f91f'
auth_token = '7eb697e8c170c5950e4f21f0d2a5c00f'
twilio_phone_number = '+12057820889'

init = True
if init:
    client = Client(account_sid, auth_token)
    init = False