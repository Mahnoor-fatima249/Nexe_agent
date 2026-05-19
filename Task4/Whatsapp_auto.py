import os
import datetime
from groq import Groq
from dotenv import load_dotenv

# 1. Configuration
load_dotenv()
GROQ_API_KEY = str(os.getenv("GROQ_API_KEY"))
client = Groq(api_key=GROQ_API_KEY)

# 2. FAQ Data (Aap is mein mazeed sawal add kar sakti hain)
FAQ_DATA = {
    "timing": "Hamara office subah 9 se shaam 5 baje tak khula hota hai.",
    "services": "Hum AI Automation, Web Development, aur Chatbot services dete hain.",
    "location": "Hamara main office Islamabad, Pakistan mein hai.",
    "internship": "Nexe-Agent internship program Gen-AI par focus karta hai."
}

def log_conversation(user_msg, bot_reply):
    """Requirement: Har baat ka record save karna"""
    with open("whatsapp_chats.log", "a", encoding="utf-8") as f:
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{t}] USER: {user_msg}\n[{t}] BOT: {bot_reply}\n{'-'*30}\n")

def get_ai_reply(user_input):
    """Requirement: FAQ-based aur AI Auto-Reply logic"""
    user_input = user_input.lower()

    # Check if it's an FAQ
    for key in FAQ_DATA:
        if key in user_input:
            return FAQ_DATA[key]

    # Agar FAQ nahi hai, toh AI se reply lo (Auto-Reply System)
    try:
        prompt = f"You are a helpful WhatsApp Assistant. Reply to this user message shortly: {user_input}"
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except:
        return "G ma'am, main aapki kya madad kar sakta hoon?"

def start_whatsapp_bot():
    print("\n--- 🤖 Nexe-Agent WhatsApp AI Bot (Simulation) ---")
    print("Type 'exit' to stop the bot.\n")

    while True:
        user_msg = input("Incoming Message: ")
        if user_msg.lower() == 'exit':
            break

        print("🔄 Bot is typing...")
        reply = get_ai_reply(user_msg)
        
        print(f"Reply Sent: {reply}")
        
        # Conversation log karna
        log_conversation(user_msg, reply)

if __name__ == "__main__":
    start_whatsapp_bot()
