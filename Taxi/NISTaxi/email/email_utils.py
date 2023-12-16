
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from NISTaxi.email.config import *

def send_email(receiver_email : str, subject : str, body : str):
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server.sendmail(sender_email, receiver_email, msg.as_string())