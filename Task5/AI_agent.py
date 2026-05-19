import os
import smtplib
from email.message import EmailMessage
from groq import Groq
from duckduckgo_search import DDGS
from dotenv import load_dotenv

# --- CONFIGURATION & KEYS ---
# Is line se Python usi folder mein .env dhoondega jahan ye script hai
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Agar .env phir bhi na chale to ye line error se bachayegi
if not GROQ_API_KEY:
    # Option: Agar .env kaam na kare to yahan apni key paste kar dein
    GROQ_API_KEY =   "GROQ_API_KEY"

client = Groq(api_key=GROQ_API_KEY)

# --- TOOL 1: Web Search ---
def search_web(query):
    """Internet se latest information nikalne ke liye"""
    print(f"\n🔍 Agent is searching the web for: '{query}'...")
    results_text = ""
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            results_text = "\n".join(results)
    except Exception as e:
        results_text = f"Search failed: {e}"
    return results_text

# --- TOOL 2: Save Notes ---
def save_notes(content, filename="agent_research.txt"):
    """Research ko file mein save karne ke liye"""
    print(f"📝 Saving research to {filename}...")
    try:
        with open(filename, "a", encoding="utf-8") as f:
            import datetime
            time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"\n{'='*50}\nResearch Date: {time_now}\n{'='*50}\n{content}\n")
        return "✅ Notes saved successfully."
    except Exception as e:
        return f"❌ Failed to save notes: {e}"

# --- TOOL 3: Send Email ---
def send_email(receiver, body):
    """Final report email karne ke liye"""
    print(f"📧 Sending report to {receiver}...")
    sender = "mf0488789@gmail.com"
    password = "ipusgxdeennuhsjf" 
    
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = "Nexe-Agent: Multi-Tool AI Research Report"
    msg['From'] = sender
    msg['To'] = receiver
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        return "✅ Email sent successfully."
    except Exception as e:
        return f"❌ Email error: {e}"

# --- MAIN AGENT EXECUTION ---
def run_multi_tool_agent():
    print("\n--- 🤖 Nexe-Agent Multi-Tool AI Agent (Advanced) ---")
    
    user_query = input("\nWhat do you want me to research? ")
    target_email = input("Enter email to send the report: ")

    # Step 1: Web Search
    raw_data = search_web(user_query)

    # Step 2: AI Processing (Summarization)
    print("🧠 AI is analyzing and summarizing the data...")
    prompt = f"""
    You are an Advanced AI Agent. Analyze the following raw search data and create a 
    professional, detailed report.
    Topic: {user_query}
    Raw Data: {raw_data}
    The report should include a Summary, Key Findings, and a Conclusion.
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        final_report = completion.choices[0].message.content

        # Step 3: Tool Usage
        note_status = save_notes(final_report)
        email_status = send_email(target_email, final_report)

        print("\n" + "="*50)
        print("🚀 TASK COMPLETED SUCCESSFULLY!")
        print("="*50)
        print(f"1. {note_status}")
        print(f"2. {email_status}")
        
    except Exception as e:
        print(f"\n❌ Error during AI generation: {e}")

if __name__ == "__main__":
    run_multi_tool_agent()
