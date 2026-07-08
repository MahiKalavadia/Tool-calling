from langchain_core.tools import tool

@tool
def add_note(query:str):
    """Add the notes"""
    with open("notes.json","a") as f:
        f.write(query)
    return "Note added successfully!"

@tool
def view_notes(query:str):
    """View the notes"""
    with open("notes.json","r") as f:
        f.read(query)
    return "Note viewed successfully!"

@tool
def add_task(query:str):
    """Add the tasks"""
    with open("tasks.json","a") as f:
        f.write(query)
    return "Task added successfully!"

@tool
def view_tasks(query:str):
    """View the tasks"""
    with open("tasks.json","a") as f:
        f.read(query)
    return "Task viewed successfully"

