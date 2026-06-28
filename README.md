# 📄 Production RAG Chatbot

A production-ready Retrieval-Augmented Generation (RAG) chatbot built with Python, Streamlit, LangChain, FAISS, BM25, Hugging Face Embeddings, and Groq LLM.

## 🚀 Features

* Multi-PDF Upload
* Hybrid Retrieval (FAISS + BM25)
* Context-aware Question Answering
* General AI Chat (fallback)
* Conversation Memory
* Streaming Responses
* Source Citation
* Variable Extraction from PDFs
* Groq LLM Integration

## 🛠 Tech Stack

* Python
* Streamlit
* LangChain
* FAISS
* BM25
* Hugging Face Embeddings
* Groq API
* PyMuPDF

## 📂 Project Structure

```
production-rag-chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── core/
│   ├── loader.py
│   ├── chunker.py
│   ├── retriever.py
│   ├── llm_engine.py
│   ├── answer_engine.py
│   └── ...
```

## ▶️ Installation

```bash
git clone https://github.com/aashishwadbude8-droid/production-rag-chatbot.git
cd production-rag-chatbot

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
```

## 📸 Screenshots

(Add screenshots here)

## 👨‍💻 Author

Aashish Wadbude
