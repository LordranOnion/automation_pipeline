# config.py
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

WAZUH_URL = os.getenv("WAZUH_URL")
WAZUH_USER = os.getenv("WAZUH_USER")
WAZUH_PASS = os.getenv("WAZUH_PASS")

CALDERA_URL = os.getenv("CALDERA_URL")
CALDERA_API_KEY = os.getenv("CALDERA_API_KEY")
CALDERA_AGENT_GROUP = os.getenv("CALDERA_AGENT_GROUP")
