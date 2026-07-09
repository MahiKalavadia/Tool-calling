import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from schema import ChatRequest, ChatResponse
from dotenv import load_dotenv
from agents import agent
from langfuse import get_client
from langfuse.langchain import CallbackHandler

load_dotenv()

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_formatter = logging.Formatter(
    "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

log_filename = f"app_{datetime.today().strftime('%Y-%m-%d')}.log"
file_handler = logging.FileHandler(
    os.path.join(LOG_DIR, log_filename),
    encoding="utf-8",
)
file_handler.setFormatter(log_formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[console_handler, file_handler],
)

logging.getLogger("watchfiles").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

langfuse = get_client()
langfuse_handler = CallbackHandler()

app = FastAPI(
    title="AI Agent API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "AI Agent API is running."}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        logger.info(f"User Query: {request.query}")

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": request.query,
                    }
                ]
            },
            config={
                "callbacks": [langfuse_handler]
            },
        )

        answer = response["messages"][-1].content

        logger.info("Agent responded successfully")

        return ChatResponse(response=answer)

    except Exception as e:
        logger.exception("Error while invoking agent")
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    finally:
        try:
            langfuse.flush()
            logger.info("Langfuse flushed successfully")
        except Exception:
            logger.warning("Failed to flush Langfuse")