from langchain_core.tools import tool
import json
import logging
import os
from schema import NoteSchema, TaskSchema

logger = logging.getLogger(__name__)

NOTES_FILE = "notes1.json"
TASKS_FILE = "tasks1.json"


def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, "r") as f:
            content = f.read().strip()
        if not content:
            return []
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to load notes json: {e}")
        return []


def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4)


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r") as f:
            content = f.read().strip()
        if not content:
            return []
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to load tasks json: {e}")
        return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


@tool(args_schema=NoteSchema)
def note_add(note: str) -> str:
    """Add a note."""
    try:
        logger.info("note_add tool called")
        notes = load_notes()
        notes.append({
            "id": len(notes) + 1,
            "note": note,
        })
        save_notes(notes)
        logger.info("Note added successfully")
        return "Note saved successfully!"
    except Exception as e:
        logger.exception(f"Failed to add note: {e}")
        return "An error occurred while saving the note."


@tool()
def note_view(_: str = "") -> str:
    """View all notes."""
    try:
        logger.info("note_view tool called")
        notes = load_notes()
        if not notes:
            return "No notes found."
        formatted_notes = "\n".join(
            f"{i + 1}. {note['note']}" for i, note in enumerate(notes)
        )
        return formatted_notes
    except Exception as e:
        logger.exception(f"Failed to view notes: {e}")
        return "An error occurred while retrieving notes."


@tool(args_schema=TaskSchema)
def task_add(task: str) -> str:
    """Add a task."""
    try:
        logger.info("task_add tool called")
        tasks = load_tasks()
        tasks.append({
            "id": len(tasks) + 1,
            "task": task,
            "status": "pending",
        })
        save_tasks(tasks)
        logger.info("Task added successfully")
        return "Task saved successfully!"
    except Exception as e:
        logger.exception(f"Failed to add task: {e}")
        return "An error occurred while saving the task."


@tool()
def task_view(_: str = "") -> str:
    """View all tasks."""
    try:
        logger.info("task_view tool called")
        tasks = load_tasks()
        if not tasks:
            return "No tasks found."
        formatted_tasks = "\n".join(
            f"{i + 1}. {task['task']} - {task['status']}" for i, task in enumerate(tasks)
        )
        return formatted_tasks
    except Exception as e:
        logger.exception(f"Failed to view tasks: {e}")
        return "An error occurred while retrieving tasks."

@tool(args_schema=TaskSchema)
def change_task_status(task:str) -> str:
    """Mark an existing task as completed.

    The task parameter should be the task name or part of it, used to
    identify which task to mark as completed. It should be the normalized
    task name extracted by the LLM."""
    try:
        logger.info(f"task_status tool enabled for task: {task}")
        tasks = load_tasks()
        if not tasks:
            return "No tasks found"
        
        for t in tasks:
            if task.lower().strip() in t["task"].lower().strip():
                if t["status"] == "completed":
                    return "Task is already completed"
                t["status"] = "completed"
                save_tasks(tasks)
                logger.info(f"Task status updated for task id: {t['id']}")
                return "Task marked as completed."
        logger.info(f"No matching task found for: {task}")
        return "No matching task found."
    except Exception as e:
        logger.exception(f"Failed to update task status: {e}")
        return "An error occurred while updating task status."
