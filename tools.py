from langchain_core.tools import tool
import json, logging, os
from schema import NoteSchema, TaskSchema

logger = logging.getLogger(__name__)

NOTES_DIR = "notes.json"
TASKS_DIR = "tasks.json"

def load_notes():
    if not os.path.exists(NOTES_DIR):
        return []
    
    with open(NOTES_DIR,"r") as f:
        return json.load(f)
    
def save_notes(notes):
    with open(NOTES_DIR,"w") as f:
        logger.info(f"Saving notes..")
        return json.dump(notes,f,indent=4)

def load_tasks():
    if not os.path.exists(TASKS_DIR):
       return []

    with open(TASKS_DIR,"r") as f:
        return json.load(f)
    
def save_task(tasks):
    with open(TASKS_DIR,"w") as f:
        return json.dump(tasks,f,indent=4)

@tool(args_schema=NoteSchema)
def note_add(note:str) -> str:
    """Add the notes"""
    try:
        logger.info(f"Note enabled: ")
        notes = load_notes()
        logger.info("Notes loaded")
        notes.append({
            "id":len(notes) + 1,
            "note":note,
        })
        save_notes(notes)
        logger.info("Notes saved")
        print("Agent: Note saved!")
    except Exception as e:
        logger.warning(f"Exception occured: {str(e)}")
        print("Exception occurred")

@tool(args_schema=NoteSchema)
def note_view(note:str="") -> str:
        """View the notes"""
        try:
            logger.info(f"Tool view task enabled: ")
            notes = load_notes()
            logger.info("Notes loaded")
            if not notes:
                return []
            print("\n".join(f"{i+1}. {note['note']}" for i, note in enumerate(notes)))
        except Exception as e:
            logger.warning(f"Exception occurred: {str(e)}")
            print("Exception occurred!")

@tool(args_schema=TaskSchema)
def task_add(task:str, task_id:int="") -> str:
    """Add the task"""
    try:
        logger.info(f"Task tool enabled:")
        tasks = load_tasks()
        logger.info("Task loaded")
        tasks.append({
            "id":len(tasks) + 1,
            "task":task,
            "status":"pending"
        })
        save_task(tasks)
        logger.info("Tasks saved")
        print("Agent: Task added successfully!")
    except FileNotFoundError as e:
        logger.warning(f"File not found: {str(e)}")
        print("File not found")
    except Exception as e:
        logger.warning(f"Exception occurred: {str(e)}")
        print("Exception occurred")

@tool
def task_view(_:str=""):
    """View the task"""
    try:
        logger.info(f"Task view enabled: ")
        tasks = load_tasks()
        logger.info(f"Tasks loaded..{tasks}")
        if not tasks:
            logger.warning("Tasks not found")
            return []
        
        print("\n".join(f"{i+1}. {task['task']}" for i, task in enumerate(tasks)))
    except Exception as e:
        logger.warning(f"Exception occurred: {str(e)}")

@tool()
def task_status(task_id:int) -> str:
    """Change the status of the already present tasks"""
    try:
        tasks = load_tasks()
        logger.info("Tasks loaded..")
        for t in tasks:
            if t["id"] == task_id:
                t["status"] = "completed"
                save_task(tasks)
                logger.info("Task saved..")

        return {"Agent":"Status changed"}
    except Exception as e:
        logger.warning(f"Exception occurred: {str(e)}")
        print("Exception occurred")
