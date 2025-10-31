from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from langgraph_database_backend import chatbot, retrieve_all_threads
import uuid


app = FastAPI(title="Langraph Chatbot API")


# Allow frontend apps (like Streamlit or React) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Models ----------------

class ChatInput(BaseModel):
    message: str
    thread_id: str | None = None

class ThreadResponse(BaseModel):
    thread_id: str
    response: str



# ---------------- Helper ----------------

def generate_thread_id():
    return str(uuid.uuid4())


# ---------------- Routes ----------------

@app.get("/")
def root():
    return {"message": "Langraph Chatbot API is running 🚀"}

@app.get("/threads")
def get_threads():
    threads = retrieve_all_threads()
    return {"threads": threads}

@app.post("/chat", response_model=ThreadResponse)
def chat(data: ChatInput):
    thread_id = data.thread_id or generate_thread_id()


    CONFIG = {
        "configurable": {"thread_id": thread_id},
        "metadata": {"thread_id": thread_id},
        "run_name": "chat_turn",
    }


    ##Run Chatbot

    messages = [{"role": "user", "content": data.message}]
    response_text = ""

    for message_chunk, metadata in chatbot.stream(
        {"messages": [HumanMessage(content=data.message)]},
        config=CONFIG,
        stream_mode="messages"
    ):
        response_text += message_chunk.content
    return ThreadResponse(thread_id=thread_id, response=response_text)