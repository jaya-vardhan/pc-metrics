import os
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mailer:

    def __init__(self):
        self.MAIL_USERNAME = os.getenv("MAIL_USERNAME")
        self.MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
        self.RECIEPETANT_MAIL = os.getenv("RECIEPETANT_MAIL")

    def send(self, mail_body):
        if os.getenv('ENABLE_ALERTS').lower() == 'true':
            try:
                message = MIMEMultipart()
                message["Subject"] = "Pc Metrics"
                message["From"] = self.MAIL_USERNAME
                message["To"] = self.RECIEPETANT_MAIL
                body = json.dumps(mail_body)
                message.attach(MIMEText(body, "plain"))
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(self.MAIL_USERNAME, self.MAIL_PASSWORD)
                    server.sendmail(self.MAIL_USERNAME, self.RECIEPETANT_MAIL, message.as_string())
            except Exception as e:
                print(str(e))
            else:
                print("mail send")
        else:
            print("Please Enable Alerts :)")
