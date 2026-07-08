import logging, os
from datetime import datetime
from agents import agent
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from dotenv import load_dotenv

load_dotenv()
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

log_filename = f"app_{datetime.today().strftime('%Y-%m-%d')}.log"
file_handler = logging.FileHandler(filename=os.path.join(LOG_DIR, log_filename))
file_handler.setFormatter(log_formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[console_handler,file_handler]
)

logging.getLogger("watchfiles").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

langfuse = get_client()

langfuse_handler = CallbackHandler()

query = input("User: ")
response = agent.invoke({
    'messages':[{
        'role':'user',
        'content':query
    }]
},
config={
    'callbacks':[langfuse_handler]
}
)