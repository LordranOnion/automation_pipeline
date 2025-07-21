# ollama_api.py
import requests
import os
import json
from config import OLLAMA_URL, OLLAMA_MODEL

def generate_wazuh_rule(nl_attack=None, logs=None):
    if nl_attack:
        prompt = (
            f"Given the following attack scenario described in natural language, generate a Wazuh SIEM detection rule (in XML) to detect this attack:\n\n"
            f"Attack Description: {nl_attack}\n"
        )
    elif logs:
        prompt = (
            f"Given the following Wazuh log entries, generate a new Wazuh SIEM detection rule (in XML) that can detect this or similar attacks in the future:\n\n"
            f"Log Entries:\n{logs}\n"
        )
    else:
        raise ValueError("Must provide nl_attack or logs.")

    # Ollama expects a JSON payload with 'model' and 'prompt'
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False  # If True, handle the response as a stream (optional)
    }

    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=360)
    response.raise_for_status()

    result = response.json()
    rule = result.get("response", "")
    return rule.strip()
