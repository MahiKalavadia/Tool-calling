from langchain_core.tools import tool
import json, logging, os
from schema import NoteSchema, TaskSchema, TaskViewSchema, NoteViewSchema, Note

logger = logging.getLogger(__name__)

NOTES_FILES = "notes.json"
TASKS_FILES = "tasks.json"

def load_notes():
    if not os.path.exists(NOTES_FILES):
        return []
    try:
        with open(NOTES_FILES,"r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to load json {e}")
    
def save_notes(notes):
    with open(NOTES_FILES,"w") as f:
        json.dump(notes, f, indent=4)

def load_tasks():
    if not os.path.exists(TASKS_FILES):
       return []
    try:
        with open(TASKS_FILES,"r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to load json {e}")

    
def save_task(tasks):
    with open(TASKS_FILES,"w") as f:
        json.dump(tasks, f, indent=4)

@tool(args_schema=NoteSchema)
def note_add(note:str) -> str:
    """Only Add the notes"""
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
        return {
            "message":"Note saved successfully!"
        }
    except FileNotFoundError as e:
        logger.exception(f"Note file not found: {e}")
        return "Note file not found."
    except Exception as e:
        logger.exception(f"Failed to add note: {e}")
        return "An error occurred while saving the note."

@tool(args_schema=NoteSchema)
def note_view(_:str="") -> dict:
    """Only View the notes"""
    try:
        logger.info("note_view tool enabled")
        notes = load_notes()
        logger.debug(f"Loaded notes: {len(notes)}")
        if not notes:
            logger.info("No notes found")
            return "No notes found."
        logger.info("Notes retrieved successfully")
        return {
            "note": notes
        }
    except FileNotFoundError as e:
        logger.exception(f"Note file not found: {e}")
        return "Note file not found."
    except Exception as e:
        logger.exception(f"Failed to view notes: {e}")
        return "An error occurred while retrieving notes."

@tool(args_schema=TaskSchema)
def task_add(task:str) -> str:
    """Only Add the task"""
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
        return {
            "message":"Task saved successfully!"
        }
    except FileNotFoundError as e:
        logger.exception(f"Task file not found: {e}")
        return "Task file not found."
    except Exception as e:
        logger.exception(f"Failed to add task: {e}")
        return "An error occurred while saving the task."

@tool(args_schema=TaskSchema)
def task_view(_:str="") -> dict:
    """Only view the task"""
    try:
        logger.info("task_view tool enabled")
        tasks = load_tasks()
        logger.debug(f"Loaded tasks: {len(tasks)}")
        if not tasks:
            logger.info("No tasks found")
            return "No tasks found."
        logger.info("Tasks retrieved successfully")
        return {
            "task":tasks
        }
    except FileNotFoundError as e:
        logger.exception(f"Task file not found: {e}")
        return "Task file not found."
    except Exception as e:
        logger.exception(f"Failed to view tasks: {e}")
        return "An error occurred while retrieving tasks."

@tool(args_schema=TaskSchema)
def change_task_status(task:str) -> str:
    """Match the task user entered with the task available in file and change its status"""
    try:
        logger.info(f"task_status tool enabled for task: {task}")
        tasks = load_tasks()
        for t in tasks:
            if task.lower() in t["task"].lower():
                t["status"] = "completed"
                save_task(tasks)
                logger.info(f"Task status updated for task id: {t['id']}")
                return {
                    "status":"completed",
                    "task":t["task"],
                    "status":t["status"]
                }
        logger.info(f"No matching task found for: {task}")
        return "No matching task found."
    except Exception as e:
        logger.exception(f"Failed to update task status: {e}")
        return "An error occurred while updating task status."
