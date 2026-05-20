import os
import numpy as np
from flask import Flask, render_template_string, request, jsonify
from groq import Groq
from dotenv import load_dotenv
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

load_dotenv()
app = Flask(__name__)

# Master API Key Setup
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# Task 6 (RAG) ke liye model embedding initialize
print("⏳ Loading Embedding Model for Dashboard...")
try:
    embed_model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Embedding model error: {e}")
    embed_model = None

# --- MASTER DASHBOARD UI ---
HTML_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <title>Nexe-Agent GenAI Portfolio</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #f0f2f5; margin: 0; padding: 0; display: flex; height: 100vh; }
        .sidebar { width: 260px; background: #1e293b; color: white; padding: 20px; display: flex; flex-direction: column; gap: 10px; }
        .sidebar h2 { font-size: 1.2rem; margin-bottom: 20px; color: #38bdf8; text-align: center; }
        .nav-btn { background: none; border: none; color: #94a3b8; padding: 12px; text-align: left; border-radius: 6px; cursor: pointer; font-size: 0.95rem; font-weight: 500; transition: 0.3s; }
        .nav-btn:hover, .nav-btn.active { background: #334155; color: white; }
        .main-content { flex: 1; padding: 30px; display: flex; flex-direction: column; overflow-y: auto; }
        .card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); height: 80vh; display: none; flex-direction: column; }
        .card.active { display: flex; }
        /* Chat UI styles */
        .chat-box { flex: 1; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; overflow-y: auto; margin-bottom: 15px; background: #f8fafc; }
        .msg { margin-bottom: 10px; padding: 10px; border-radius: 6px; max-width: 80%; line-height: 1.4; }
        .user { background: #0284c7; color: white; margin-left: auto; }
        .bot { background: #e2e8f0; color: #1e293b; }
        .input-row { display: flex; gap: 10px; }
        input, select, textarea { flex: 1; padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px; outline: none; }
        button.action-btn { background: #0284c7; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; }
        button.action-btn:hover { background: #0369a1; }
    </style>
</head>
<body>

    <div class="sidebar">
        <h2>Nexe Portfolio 🚀</h2>
        <button class="nav-btn active" onclick="showTask('home')">🏠 Dashboard Home</button>
        <button class="nav-btn" onclick="showTask('task1')">🤖 Task 1: AI Chatbot</button>
        <button class="nav-btn" onclick="showTask('task3')">📄 Task 3: Resume Screener</button>
        <button class="nav-btn" onclick="showTask('task6')">🏢 Task 6: RAG Assistant</button>
    </div>

    <div class="main-content">
        <div id="home" class="card active">
            <h2>Welcome Mahnoor Fatima! 👋</h2>
            <p>Yeh aapka central deployment hub hai jahan aapke saare GenAI projects ek hi link par live chal rahe hain.</p>
            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 20px 0;">
            <h3>Internship Progress Summary:</h3>
            <ul>
                <li><strong>Task 1:</strong> Chatbot Core (Live Interface)</li>
                <li><strong>Task 3:</strong> Contextual Resume Parser & Matcher</li>
                <li><strong>Task 6:</strong> Corporate Knowledge Base (RAG Pipeline)</li>
            </ul>
        </div>

        <div id="task1" class="card">
            <h2>🤖 Task 1: AI Chatbot (Llama 3.1)</h2>
            <div class="chat-box" id="chatBox1"></div>
            <div class="input-row">
                <input type="text" id="input1" placeholder="Ask the chatbot anything..." onkeypress="if(event.keyCode===13) sendChat()">
                <button class="action-btn" onclick="sendChat()">Send</button>
            </div>
        </div>

        <div id="task3" class="card">
            <h2>📄 Task 3: Smart Resume Screener</h2>
            <p>Enter the candidate profile summary and the Target Job Description below:</p>
            <textarea id="resumeText" placeholder="Paste Resume text or Candidate details here..." style="height: 100px; margin-bottom: 10px; width:97%; padding:10px; border-radius:6px; border:1px solid #cbd5e1;"></textarea>
            <textarea id="jdText" placeholder="Paste Job Description here..." style="height: 100px; margin-bottom: 15px; width:97%; padding:10px; border-radius:6px; border:1px solid #cbd5e1;"></textarea>
            <button class="action-btn" onclick="screenResume()">Screen & Score Resume</button>
            <div id="screenerResult" style="margin-top: 15px; padding: 15px; background: #f8fafc; border-left: 4px solid #0284c7; border-radius:4px; white-space: pre-line; overflow-y:auto; flex:1;">Results will appear here...</div>
        </div>

        <div id="task6" class="card">
            <h2>🏢 Task 6: RAG Company Knowledge Base</h2>
            <p>Ask questions based on company policies (Using Fallback Simulation Database):</p>
            <div class="chat-box" id="chatBox6">
                <div class="msg bot">System Initialized with Nexe-Agent Policy Manual. Ask me about timings, office location, or leaves.</div>
            </div>
            <div class="input-row">
                <input type="text" id="input6" placeholder="Ask about company rules..." onkeypress="if(event.keyCode===13) askRAG()">
                <button class="action-btn" onclick="askRAG()">Query Docs</button>
            </div>
        </div>
    </div>

    <script>
        function showTask(id) {
            document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(id).classList.add('active');
            event.target.classList.add('active');
        }

        // --- TASK 1 BACKEND INTERACTION ---
        async function sendChat() {
            const input = document.getElementById('input1');
            const text = input.value.trim();
            if(!text) return;
            appendMsg('chatBox1', text, 'user');
            input.value = '';

            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ message: text })
            });
            const data = await res.json();
            appendMsg('chatBox1', data.reply, 'bot');
        }

        // --- TASK 3 BACKEND INTERACTION ---
        async function screenResume() {
            const resume = document.getElementById('resumeText').value;
            const jd = document.getElementById('jdText').value;
            const output = document.getElementById('screenerResult');
            if(!resume || !jd) { alert('Please fill both fields!'); return; }
            output.innerText = "Processing context and generating scorecard...";

            const res = await fetch('/api/screener', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ resume: resume, jd: jd })
            });
            const data = await res.json();
            output.innerText = data.reply;
        }

        // --- TASK 6 BACKEND INTERACTION ---
        async function askRAG() {
            const input = document.getElementById('input6');
            const text = input.value.trim();
            if(!text) return;
            appendMsg('chatBox6', text, 'user');
            input.value = '';

            const res = await fetch('/api/rag', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ query: text })
            });
            const data = await res.json();
            appendMsg('chatBox6', data.reply, 'bot');
        }

        function appendMsg(boxId, text, type) {
            const box = document.getElementById(boxId);
            const div = document.createElement('div');
            div.className = `msg ${type}`;
            div.innerText = text;
            box.appendChild(div);
            box.scrollTop = box.scrollHeight;
        }
    </script>
</body>
</html>
"""

# --- ROUTES ---
@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    msg = request.json.get('message')
    try:
        comp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": msg}])
        return jsonify({"reply": comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

@app.route('/api/screener', methods=['POST'])
def api_screener():
    resume = request.json.get('resume')
    jd = request.json.get('jd')
    prompt = f"Analyze this Resume:\n{resume}\n\nAgainst this Job Description:\n{jd}\n\nProvide a Match Percentage, Missing Skills, and Hiring Recommendation."
    try:
        comp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}])
        return jsonify({"reply": comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

@app.route('/api/rag', methods=['POST'])
def api_rag():
    query = request.json.get('query')
    # Simulation Data Chunks (Task 6 backend fallback logic)
    chunks = [
        "Nexe-Agent office timings are from 9:00 AM to 5:00 PM, Monday to Friday.",
        "The company main head office is located in Islamabad, Pakistan.",
        "Nexe-Agent provides services in Gen-AI Automation, Web Development, and Custom Chatbots.",
        "Employees are allowed a maximum of 15 annual leaves per calendar year."
    ]
    try:
        if embed_model:
            q_embed = embed_model.encode([query])
            c_embeds = embed_model.encode(chunks)
            sims = np.dot(c_embeds, q_embed.T).flatten()
            context = chunks[np.argmax(sims)]
        else:
            context = chunks[0] # Fallback if model loading skipped
        
        prompt = f"Context: {context}\nQuestion: {query}\nAnswer the question directly using the context. If not found, say you don't know."
        comp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}])
        return jsonify({"reply": comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
