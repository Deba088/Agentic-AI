from dotenv import load_dotenv
import requests
from agents import function_tool
import os
import smtplib
from email.message import EmailMessage

load_dotenv(override=True)

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"


@function_tool
def send_email_notification(subject: str, text_body: str, html_body: str = None):
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = "debanjang0.dg@gmail.com"
    msg["Subject"] = subject
    msg.set_content(text_body)
    if html_body:
        msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(EMAIL_SMTP_SERVER, 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        server.send_message(msg)

    payload = {"user": pushover_user, "token": pushover_token, "message": text_body, "title": subject}
    requests.post(url=pushover_url, data=payload)
