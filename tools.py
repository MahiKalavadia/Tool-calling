from langchain_core.tools import tool
import json
import logging
from langchain_groq import ChatGroq
import os
from schema import NoteSchema, TaskSchema
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
llm = ChatGroq(model="llama-3.3-70b-versatile")

NOTES_DIRS = "notes"
TASKS_DIRS = "tasks"

os.makedirs(NOTES_DIRS, exist_ok=True)
os.makedirs(TASKS_DIRS, exist_ok=True)

note_filename = "notes.json"
task_filename = "tasks.json"

def load_notes():
    if not os.path.exists(os.path.join(NOTES_DIRS, note_filename)):
        return []
    try:
        with open(os.path.join(NOTES_DIRS, note_filename), "r") as f:
            content = f.read().strip()
        if not content:
            return []
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to load notes json: {e}")
        return []


def save_notes(notes):
    with open(os.path.join(NOTES_DIRS, note_filename), "w") as f:
        json.dump(notes, f, indent=4)


def load_tasks():
    if not os.path.exists(os.path.join(TASKS_DIRS, task_filename)):
        return []
    try:
        with open(os.path.join(TASKS_DIRS, task_filename), "r") as f:
            content = f.read().strip()
        if not content:
            return []
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to load tasks json: {e}")
        return []


def save_tasks(tasks):
    with open(os.path.join(TASKS_DIRS, task_filename), "w") as f:
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
        logger.error(f"Failed to add note: {str(e)}")
        return "An error occurred while saving the note."


@tool()
def note_view(_: str = "") -> str:
    """Load all the notes available"""
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
        logger.error(f"Failed to view notes: {str(e)}")
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
        logger.error(f"Failed to add task: {str(e)}")
        return "An error occurred while saving the task."


@tool()
def task_view(_: str = "") -> str:
    """Load all the tasks present."""
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
        logger.error(f"Failed to view tasks: {str(e)}")
        return "An error occurred while retrieving tasks."

@tool(args_schema=TaskSchema)
def change_task_status(task: str) -> dict:
    """
    Mark an existing task as completed.

    This tool should be used only when the user indicates they have completed
    or finished a previously created task or it is like a statement in past tense .

    Workflow:
    1. Load all existing tasks.
    2. Send the user's statement and task list to the LLM.
    3. The LLM identifies the best matching task ID.
    4. Update that task's status to 'completed'.
    """

    try:
        logger.info(f"Finding task for: {task}")
        tasks = load_tasks()
        if not tasks:
            return "No tasks found."

        prompt = f"""
            You are a task matching assistant.

            User statement:
            "{task}"

            Existing tasks:
            {json.dumps(tasks, indent=2)}

            Instructions:
            - Identify the task that best matches the user's statement.
            - Return ONLY the task ID as an integer.
            - Do not explain your answer.
            """

        llm_response = llm.invoke([HumanMessage(content=prompt)])
        task_id = int(llm_response.content.strip())
        if task_id == -1:
            return "No matching task found."

        for t in tasks:
            if t["id"] == task_id:
                if t["status"] == "completed":
                    return "Task is already completed."

                t["status"] = "completed"
                save_tasks(tasks)

                logger.info(f"Task {task_id} marked as completed.")

                return "Task marked as completed."

        return "Task ID returned by LLM does not exist."

    except ValueError:
        logger.error("LLM did not return a valid integer.")
        return "Failed to identify the task."

    except Exception as e:
        logger.error(f"Failed to update task status. {str(e)}")
        return "Failed to update task status"