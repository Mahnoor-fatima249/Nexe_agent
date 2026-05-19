import os
import PyPDF2
from groq import Groq
from dotenv import load_dotenv

# 1. Load Keys
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
client = Groq(api_key=GROQ_API_KEY)

def extract_text_from_pdf(pdf_path):
    """PDF file se text nikalne ke liye"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def screen_resume(resume_text, job_description):
    """AI logic jo Resume aur Job ko compare karega"""
    prompt = f"""
    You are an expert HR Recruiter. Compare the following Resume with the Job Description.
    
    Job Description:
    {job_description}
    
    Resume Text:
    {resume_text}
    
    Please provide:
    1. Match Percentage (0-100%)
    2. Key Skills Found
    3. Missing Skills
    4. Final Verdict (Short summary)
    """
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

def main():
    print("\n--- Nexe-Agent Resume Screener AI ---")
    
    # PDF file ka naam yahan sahi se likhein
    pdf_name = input("Enter your PDF file name (e.g., cv.pdf): ")
    
    # Job Description (JD) yahan input karein
    jd = input("Enter the Job Description (e.g., Python Developer with AI skills): ")

    if os.path.exists(pdf_name):
        print("\n[Step 1] Extracting text from Resume...")
        resume_content = extract_text_from_pdf(pdf_name)
        
        print("[Step 2] Analyzing with AI...")
        report = screen_resume(resume_content, jd)
        
        print("\n" + "="*40)
        print("📋 AI SCREENING REPORT")
        print("="*40)
        print(report)
    else:
        print("❌ Error: File nahi mili! Check karein ke naam sahi hai.")

if __name__ == "__main__":
    main()
