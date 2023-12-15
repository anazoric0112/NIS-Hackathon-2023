from twilio.rest import Client

account_sid = 'AC5976d2495214230258657c24c4ed7e89'
auth_token = '58f9783adfa17e03ce3aeb8562c2a9d1'
twilio_phone_number = '+14314415765'

init = True
if init:
    client = Client(account_sid, auth_token)
    init = False