from langchain.agents import create_agent
from tools import note_add, task_add, note_view, task_view, task_status
from langchain_groq import ChatGroq
from prompts import prompt
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()
model=ChatGroq(model="llama-3.3-70b-versatile")

tools = [note_view, note_add, task_view, task_add, task_status]
logger.info(f"Tools available: {tools}")
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=prompt
    )