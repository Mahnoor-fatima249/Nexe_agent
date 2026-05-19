# 🏢 Nexe-Agent Company Knowledge Assistant (RAG System)

An Advanced Generative AI application built during my internship at **Nexe-Agent**. This project implements a **Retrieval-Augmented Generation (RAG)** pipeline that allows users to query custom company documentation (PDFs/Text) and receive context-grounded, precise answers using Open-Source LLMs via Groq.

---

## 🚀 Features
- **Document Processing:** Efficient text extraction from local documents using the `pypdf` library.
- **Vector Embeddings:** Semantic representation of text chunks using `Sentence-Transformers` (`all-MiniLM-L6-v2`).
- **Intelligent Retrieval:** Mathematical context matching powered by `NumPy` computing similarity vectors.
- **Grounded Responses:** Query execution via **Groq API (Llama 3.1 8B Instant)** to eliminate AI hallucinations.
- **Fail-Safe Fallback:** Embedded robust error handling that triggers a simulation dataset if the source document is corrupted.

---

## 🛠️ Tech Stack
- **Language:** Python 3.14
- **LLM Inference:** Groq Cloud SDK (Llama-3.1-8b-instant)
- **Embeddings Model:** Hugging Face `all-MiniLM-L6-v2`
- **Data & Math Libraries:** NumPy
- **File Parsing:** pypdf

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/nexe-agent-task6.git](https://github.com/your-username/nexe-agent-task6.git)
cd nexe-agent-task6

