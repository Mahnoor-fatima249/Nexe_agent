import smtplib
import ssl
import os
from dotenv import load_dotenv
import datetime
from email.message import EmailMessage
from groq import Groq
load_dotenv()

# --- CONFIGURATION ---
SENDER_EMAIL = "mf0488789@gmail.com" 
APP_PASSWORD = "PASSWORD"
GROQ_API_KEY = "GROQ_API_KEY"

client = Groq(api_key=GROQ_API_KEY)

def generate_email_content(topic):
    """Groq AI se professional email content generate karna"""
    prompt = f"Write a professional and short email about: {topic}. Keep it formal."
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

def log_email_history(receiver, subject):
    """Task Requirement: Har email ka record save karna"""
    with open("email_history.log", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] Sent to: {receiver} | Subject: {subject}\n")

def send_email():
    print("\n--- Nexe-Agent Email Automation Tool ---")
    receiver = input("Recipient Email: ")
    topic = input("Email Topic : ")

    # AI se content banwana
    print("\n[Step 1] AI is writing your email...")
    content = generate_email_content(topic)
    subject = f"Automated Update: {topic}"

    # Email message setup
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver
    msg.set_content(content)

    # Secure Connection setup
    print("[Step 2] Connecting to Gmail Server...")
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        
        # History log karna
        log_email_history(receiver, subject)
        
        print("\n" + "="*30)
        print("✅ SUCCESS: Email Sent & Logged!")
        print("="*30)
        print(f"Check 'email_history.log' for proof.")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    send_email()
