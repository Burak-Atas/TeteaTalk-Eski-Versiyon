import os
from email.message import EmailMessage
import ssl
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def random_number():
    return random.randint(100000, 999999)

class EmailVerification():
    def __init__(self,email_reciver):
        self.code = str(random_number())
        self.context = ssl.create_default_context()
        self.email_password = "oxpnfbisvcccjbud"
        self.email_sender = "noreply@teteatalk.com"
        self.email_reciver = email_reciver
        #self.em = EmailMessage()
        self.body = self.create_body()
        self.context = ssl.create_default_context()
        self.em = MIMEMultipart()
        self.em['From'] = 'TeteaTalk <{}>'.format(self.email_sender)
        self.em['To'] = self.email_reciver
        self.em['Subject'] = 'E-posta Doğrulama Kodu'
        self.em.attach(MIMEText(self.body, 'html'))
        self.send_code()

    def create_body(self):
        body = """
        <!DOCTYPE html>
            <html>
            <head>
                <title>TeteaTalk E-posta Doğrulama Kodu</title>
            </head>
            <body style="background-color: #f0f5f9; text-align: center;">
                <h1 style="font-size: 24px; color: #4285f4; margin-top: 30px;">E-posta Doğrulama Kodu</h1>
                <p style="font-size: 16px; color: #333; margin-top: 10px;">E-posta adresinizi doğrulamak için aşağıdaki kodu kullanabilirsiniz:</p>
                <h2 style="background-color: #e3f2fd; padding: 10px; display: inline-block; border-radius: 5px; font-size: 20px; color: #4285f4; margin-top: 10px;">{}</h2>
                <p style="font-size: 16px; color: #333; margin-top: 10px;">Lütfen kodu kimseyle paylaşmayınız.</p>
            </body>
            </html>

        """.format(self.code)

        return body

    def send_code(self):
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=self.context) as smtp:
            smtp.login(self.email_sender, self.email_password)
            smtp.sendmail(self.email_sender, self.email_reciver, self.em.as_string())


