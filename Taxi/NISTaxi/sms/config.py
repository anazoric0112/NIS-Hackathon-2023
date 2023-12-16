from twilio.rest import Client

account_sid = 'ACd92628dd0666c95f82391502d224f91f'
auth_token = '32ca2adb2f096c3c2e604f1d38484b88'
twilio_phone_number = '+12057820889'

init = True
if init:
    client = Client(account_sid, auth_token)
    init = False