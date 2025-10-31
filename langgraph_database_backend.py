from langgraph.graph import StateGraph, START,END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import os
import sqlite3
from typing import TypedDict, Annotated
import psycopg2

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# ---------------- LLM ----------------

llm = ChatGroq(
    api_key=api_key,
    model="llama-3.1-8b-instant"
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages': [response]}

# ---------------- Database Setup ----------------
use_postgres = os.getenv("DATABASE_URL") is not None

if use_postgres:
    import sqlalchemy
    engine = sqlalchemy.create_engine(os.getenv("DATABASE_URL"))
    conn = engine.raw_connection()

else:
    conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)

checkpointer = SqliteSaver(conn = conn)

# ---------------- Graph Setup ----------------
graph = StateGraph(ChatState)
graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)
chatbot = graph.compile(checkpointer=checkpointer)

# ---------------- Utility ----------------

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)