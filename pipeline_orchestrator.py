# pipeline_orchestrator.py
from ollama_api import generate_wazuh_rule
from wazuh_api import wazuh_authenticate, upload_wazuh_rule, fetch_wazuh_logs

def pipeline(nl_attack):
    print("Authenticating to Wazuh...")
    token = wazuh_authenticate()

    # Step 1: Generate initial rule from NL description
    print("Generating initial rule via LLM...")
    rule_xml = generate_wazuh_rule(nl_attack=nl_attack)
    print("Uploading rule to Wazuh...")
    upload_wazuh_rule(rule_xml, token)

    input("Please manually simulate the attack now, then press ENTER to continue...")
    print("Fetching logs from Wazuh...")
    logs = fetch_wazuh_logs(limit=50)
    print("Generating new rule via LLM from logs...")
    rule_xml = generate_wazuh_rule(logs=logs)
    print("Uploading rule to Wazuh...")
    upload_wazuh_rule(rule_xml, token)

    print("Pipeline completed.")

if __name__ == "__main__":

    nl_attack = input("Enter the natural language description of the initial attack: ").strip()
    if not nl_attack:
        print("No attack description provided. Exiting.")
        exit(1)
    pipeline(nl_attack)
