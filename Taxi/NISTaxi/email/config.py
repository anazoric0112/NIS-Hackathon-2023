import smtplib

smtp_server = 'smtp.gmail.com'
port = 587

sender_email = 'nistaxiservice@gmail.com'
password = 'qebk qvzs bwqt rtdu'

init = True
if init:
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender_email, password)
    init = False