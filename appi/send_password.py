import smtplib
from email.mime.text import MIMEText

def generate_new_password():
    pass

subject = 'Sosi'
body = f'Your new password {generate_new_password()}'
sender = ''
recipients = ['<EMAIL>', '<EMAIL>'] # Тут можно написать спрок адресов
password = 'pass of app gmail'

def send_gmail(subject, body, sender, recipients, password):
    pass
