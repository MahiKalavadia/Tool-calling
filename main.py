import os
import logging
from datetime import datetime
from fastapi import FastAPI
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
        start_time = datetime.now()
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
        logger.info(f"Agent Response: {response}")
        logger.info("Agent responded successfully")
        answer = response["messages"]
        logger.info(f"Agent Response: {answer}")
        end_time = datetime.now()
        logger.info(f"Latency time: {(end_time - start_time).total_seconds()} seconds")
        token_usage = response["messages"][-1].usage_metadata
        logger.info(f"Total token used: {token_usage}")

        return ChatResponse(response=response["messages"][-1].content)
    
    except Exception as e:
        logger.error(f"Error while invoking agent, error:- {str(e)}")
        return ChatResponse(response="Sorry, I'm facing a temporary issue. Please try again.")
    finally:
        try:
            langfuse.flush()
            logger.info("Langfuse flushed successfully")
        except Exception:
            logger.warning("Failed to flush Langfuse")
