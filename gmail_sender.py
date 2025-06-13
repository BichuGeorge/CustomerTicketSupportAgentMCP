import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()
import sys
sys.stdout.reconfigure(encoding='utf-8')

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
    raise ValueError("Please set EMAIL_ADDRESS and EMAIL_APP_PASSWORD in your .env file.")

print(f"Using email: {EMAIL_ADDRESS}")
print(f"Using email: {EMAIL_APP_PASSWORD}")
print("Email credentials loaded successfully.")

def send_email_smtp(to, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        print(f"Connecting to SMTP server with email: {EMAIL_ADDRESS} to send email to {to}")

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(0)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {to} with subject: {subject}")
        return {
            "status": "success",
            "message": f"Email sent to {to}"
        }
    except Exception as e:
        print(f"Error sending email: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
