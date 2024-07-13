from celery import Celery
from datetime import datetime
import smtplib
import os

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def send_email(to_address):
    # Replace these with your SMTP server details
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USERNAME = 'ogundele.damilare4@gmail.com'
    SMTP_PASSWORD = 'rismapoxjmpmktgy'

    from_address = 'ogundele.damilare4@gmail.com'
    subject = 'Test Email'
    body = 'This is a test email.'

    headers = f"From: {from_address}\r\nTo: {to_address}\r\nSubject: {subject}\r\n"
    email_message = headers + "\r\n" + body

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(from_address, to_address, email_message)

@celery.task
def log_time():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_path = '/var/log/messaging_system.log'

    with open(log_path, 'a') as log_file:
        log_file.write(f'{current_time}\n')

