# config.py
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

WAZUH_URL = os.getenv("WAZUH_URL")
WAZUH_USER = os.getenv("WAZUH_USER")
WAZUH_PASS = os.getenv("WAZUH_PASS")
WAZUH_INDEXER_URL = os.getenv("WAZUH_INDEXER_URL")

