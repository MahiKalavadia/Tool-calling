from langchain.agents import create_agent
from tools import add_note, add_task, view_notes, view_tasks
from langchain_groq import ChatGroq
from prompts import prompt
from dotenv import load_dotenv

load_dotenv()
model=ChatGroq(model="llama-3.3-70b-versatile")

tools = [add_note,add_task,view_notes, view_tasks]
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=prompt
)