# langgraph_database_backend.py
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlalchemy import SQLAlchemySaver
import os
import sqlalchemy
from typing import TypedDict, Annotated

# ---------------- Load Env ----------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
database_url = os.getenv("DATABASE_URL")

if not api_key:
    raise ValueError("GROQ_API_KEY not set in environment variables!")
if not database_url:
    raise ValueError("DATABASE_URL not set in environment variables!")

# ---------------- LLM ----------------
llm = ChatGroq(
    api_key=api_key,
    model="llama-3.1-8b-instant"
)

# ---------------- Graph & State ----------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages': [response]}

graph = StateGraph(ChatState)
graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

# ---------------- Database Setup ----------------
try:
    engine = sqlalchemy.create_engine(database_url)
    conn = engine.connect()
except Exception as e:
    print("❌ Database connection failed:", e)
    raise e

checkpointer = SQLAlchemySaver(engine=engine)

# Compile chatbot graph
chatbot = graph.compile(checkpointer=checkpointer)

# ---------------- Utility ----------------
def retrieve_all_threads():
    """
    Returns a list of all unique thread_ids stored in the database.
    """
    all_threads = set()
    try:
        for checkpoint in checkpointer.list(None):
            all_threads.add(checkpoint.config['configurable']['thread_id'])
    except Exception as e:
        print("❌ Error retrieving threads:", e)
    return list(all_threads)
