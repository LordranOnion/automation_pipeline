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

def upload_wazuh_rule(rule_xml, token, filename="custom_rules.xml"):
    url = f"{WAZUH_URL}/rules/files/{filename}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream"
    }
    # For self-signed SSL, set verify=False. Set to True in production!
    response = requests.put(url, data=rule_xml.encode('utf-8'), headers=headers, verify=False)
    response.raise_for_status()
    print(f"Rule uploaded to {url}: {response.status_code}")
    return response.json()


def fetch_wazuh_logs(token, limit=50):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{WAZUH_URL}/security/events?limit={limit}&sort=desc"
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    logs = [event["full_log"] for event in response.json()["data"]["affected_items"]]
    return '\n'.join(logs)
