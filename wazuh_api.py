# wazuh_api.py
import requests
import urllib3
import subprocess
from requests.auth import HTTPBasicAuth
from config import WAZUH_URL, WAZUH_USER, WAZUH_PASS

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def wazuh_authenticate():
    url = f"{WAZUH_URL}/security/user/authenticate"
    # Use HTTP Basic Auth, no JSON body!
    response = requests.post(url, auth=HTTPBasicAuth(WAZUH_USER, WAZUH_PASS), verify=False)
    response.raise_for_status()
    return response.json()["data"]["token"]

def upload_wazuh_rule(rule_xml):
    # Write to the local_rules.xml (append or overwrite as you need)
    with open("/var/ossec/etc/rules/local_rules.xml", "a") as f:
        f.write("\n" + rule_xml + "\n")
    # Reload or restart wazuh-manager to apply the new rule
    # subprocess.run(["systemctl", "reload", "wazuh-manager"])


def fetch_wazuh_logs(token, limit=50):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{WAZUH_URL}/security/events?limit={limit}&sort=desc"
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    logs = [event["full_log"] for event in response.json()["data"]["affected_items"]]
    return '\n'.join(logs)
