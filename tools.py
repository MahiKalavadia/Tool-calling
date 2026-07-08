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
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)
    
def save_notes(notes):
    with open(NOTES_DIR,"w") as f:
        logger.info("Saving notes..")
        json.dump(notes, f, indent=4)

def load_tasks():
    if not os.path.exists(TASKS_DIR):
       return []

    with open(TASKS_DIR,"r") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)
    
def save_task(tasks):
    with open(TASKS_DIR,"w") as f:
        json.dump(tasks, f, indent=4)

@tool(args_schema=NoteSchema)
def note_add(note:str) -> str:
    """Add the notes"""
    try:
        logger.info("note_add tool enabled")
        notes = load_notes()
        logger.debug(f"Loaded existing notes: {len(notes)}")
        notes.append({
            "id": len(notes) + 1,
            "note": note,
        })
        save_notes(notes)
        logger.info("Note added successfully")
        return "Note saved successfully."
    except FileNotFoundError as e:
        logger.warning(f"Note file not found: {e}")
        return "Note file not found."
    except Exception as e:
        logger.warning(f"Failed to add note: {e}")
        return "An error occurred while saving the note."

@tool
def note_view() -> str:
    """View the notes"""
    try:
        logger.info("note_view tool enabled")
        notes = load_notes()
        logger.debug(f"Loaded notes: {len(notes)}")
        if not notes:
            logger.info("No notes found")
            return "No notes found."
        formatted_notes = "\n".join(f"{i+1}. {note['note']}" for i, note in enumerate(notes))
        logger.info("Notes retrieved successfully")
        return formatted_notes
    except FileNotFoundError as e:
        logger.warning(f"Note file not found: {e}")
        return "Note file not found."
    except Exception as e:
        logger.warning(f"Failed to view notes: {e}")
        return "An error occurred while retrieving notes."

@tool(args_schema=TaskSchema)
def task_add(task:str) -> str:
    """Add the task"""
    try:
        logger.info("task_add tool enabled")
        tasks = load_tasks()
        logger.debug(f"Loaded existing tasks: {len(tasks)}")
        tasks.append({
            "id": len(tasks) + 1,
            "task": task,
            "status": "pending"
        })
        save_task(tasks)
        logger.info("Task added successfully")
        return "Task added successfully."
    except FileNotFoundError as e:
        logger.warning(f"Task file not found: {e}")
        return "Task file not found."
    except Exception as e:
        logger.exception(f"Failed to add task: {e}")
        return "An error occurred while saving the task."

@tool
def task_view(_:str="") -> str:
    """View the task"""
    try:
        logger.info("task_view tool enabled")
        tasks = load_tasks()
        logger.debug(f"Loaded tasks: {len(tasks)}")
        if not tasks:
            logger.info("No tasks found")
            return "No tasks found."
        formatted_tasks = "\n".join(f"{i+1}. {task['task']}" for i, task in enumerate(tasks))
        logger.info("Tasks retrieved successfully")
        return formatted_tasks
    except FileNotFoundError as e:
        logger.warning(f"Task file not found: {e}")
        return "Task file not found."
    except Exception as e:
        logger.exception(f"Failed to view tasks: {e}")
        return "An error occurred while retrieving tasks."

@tool(args_schema=TaskSchema)
def task_status(task:str) -> str:
    """Match the task user entered with the task available in file and change its status"""
    try:
        logger.info(f"task_status tool enabled for task: {task}")
        tasks = load_tasks()
        for t in tasks:
            if task.lower() in t["task"].lower():
                t["status"] = "completed"
                save_task(tasks)
                logger.info(f"Task status updated for task id: {t['id']}")
                return f"Task '{t['task']}' marked as completed."
        logger.info(f"No matching task found for: {task}")
        return "No matching task found."
    except Exception as e:
        logger.exception(f"Failed to update task status: {e}")
        return "An error occurred while updating task status."
