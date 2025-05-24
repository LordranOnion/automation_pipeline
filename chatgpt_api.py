import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

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
    response = openai.ChatCompletion.create(
        model="gpt-4.1",  # Use the latest
        messages=[{"role": "system", "content": "You are a cybersecurity analyst specializing in SIEM rule creation."},
                  {"role": "user", "content": prompt}],
        max_tokens=800
    )
    rule = response['choices'][0]['message']['content']
    return rule.strip()
