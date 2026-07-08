import logging
import os
import sys
from datetime import datetime
from agents import agent
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from dotenv import load_dotenv

load_dotenv()
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)

log_filename = f"app_{datetime.today().strftime('%Y-%m-%d')}.log"
file_handler = logging.FileHandler(filename=os.path.join(LOG_DIR, log_filename), encoding="utf-8")
file_handler.setFormatter(log_formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[console_handler, file_handler],
    force=True,
)

logging.getLogger("watchfiles").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
logger.info("Application started")

langfuse = get_client()
langfuse_handler = CallbackHandler()

try:
    query = input("User: ")
    logger.info("User query received")
    response = agent.invoke(
        {
            'messages': [
                {
                    'role': 'user',
                    'content': query
                }
            ]
        },
        config={
            'callbacks': [langfuse_handler]
        }
    )
    logger.info("Agent responded successfully")
    logger.debug("Agent response: ", response)
except Exception as e:
    logger.warning(f"Exception: {str(e)}")
finally:
    try:
        langfuse.flush()
        logger.info("Langfuse flushed successfully")
    except Exception as e:
        logger.warning(f"Failed to flush langfuse")
    logger.info("Application finished")