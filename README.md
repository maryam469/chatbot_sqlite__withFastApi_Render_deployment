# 💬 LangGraph Chatbot (FastAPI + Streamlit)

A **full-stack AI chatbot** built using **LangGraph**, **Groq LLMs**, and **FastAPI**, with a **Streamlit frontend** for real-time chat. This project supports multiple chat threads and keeps track of conversation history locally in the frontend. It’s deployable on platforms like **Render**.

---

## 🚀 Features

- Real-time chat powered by **LLaMA-3.1 Groq model**.
- Multi-thread chat support (maintains conversation per thread).
- Session-based chat history management in frontend.
- Easy integration with **FastAPI backend** and **SQLite/PostgreSQL** database.
- Streamlit UI with:
  - Sidebar for selecting previous threads
  - Chat input for user messages
  - Dynamic display of AI responses

---

## 🛠 Tech Stack

- **Backend**:  
  - Python 3.x  
  - [FastAPI](https://fastapi.tiangolo.com/)  
  - [LangGraph](https://github.com/langgraph/langgraph)  
  - [LangChain Groq](https://www.groq.com/)  
  - SQLite / PostgreSQL for checkpoints  

- **Frontend**:  
  - [Streamlit](https://chatbotappwithfastapirenderdeployment-n3qnpcndm8iqmpdhvpxags.streamlit.app/) 
  - Requests library for API communication  

- **Environment Variables**:  
  - `GROQ_API_KEY`: Your Groq API key for LLM  
  - `DATABASE_URL` *(optional)*: PostgreSQL database URL  

---

## 📦 Project Structure
langgraph-chatbot/

├─ frontend_streamlit.py # Streamlit frontend

├─ main.py # FastAPI backend

├─ langgraph_database_backend.py # LangGraph setup, LLM, and database

├─ chatbot.db # SQLite database (if used)

├─ .env # Environment variables (GROQ_API_KEY, DATABASE_URL)

└─ README.md

2. Create virtual environment (recommended)

   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows


4. Install dependencies


5. Create a .env file:
   GROQ_API_KEY=your_groq_api_key_here
   DATABASE_URL=your_postgres_url_here  

6. Run FastAPI backend
   uvicorn main:app --reload --port 8000

7. Run Streamlit frontend
   streamlit run frontend_streamlit.py


Usage

Start a new chat: Click ➕ New Chat in the sidebar.

Switch threads: Click any thread in the sidebar to view previous messages.

Send messages: Type in the chat input at the bottom and hit Enter.

View AI responses: Assistant messages appear dynamically under user messages.

Note: Previous chat threads are stored in session state; refreshing the page will clear them unless you implement a persistent backend for fetching old messages.



Limitations

Session-based storage means previous chat threads are not persistent across browser refresh.

Backend returns only the latest AI response; full thread history retrieval requires backend changes.

Groq API key is required for LLM responses.





Optional Improvements

Add a /messages/{thread_id} endpoint in backend to fetch full conversation history.

Persistent database storage for frontend threads.

Display last message snippet in sidebar like WhatsApp.

Add voice input/output using streamlit-webrtc.



📜 License

This project is MIT Licensed. Feel free to use and modify it for personal or commercial projects.



👤 Author

Maryam Faiz




🔗 References

LangGraph Documentation

LangChain Groq

Streamlit Documentation

FastAPI Documentation
