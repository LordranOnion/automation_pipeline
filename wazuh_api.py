# wazuh_api.py
import requests
import urllib3
import subprocess
from requests.auth import HTTPBasicAuth
from config import WAZUH_URL, WAZUH_USER, WAZUH_PASS, WAZUH_INDEXER_URL, WAZUH_INDEXER_USER, WAZUH_INDEXER_PASS

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def wazuh_authenticate():
    url = f"{WAZUH_URL}/security/user/authenticate"
    # Use HTTP Basic Auth, no JSON body!
    response = requests.post(url, auth=HTTPBasicAuth(WAZUH_USER, WAZUH_PASS), verify=False)
    response.raise_for_status()
    return response.json()["data"]["token"]

def upload_wazuh_rule(rule_xml, token, filename="etc/rules/local_rules.xml"):
    url = f"{WAZUH_URL}/manager/files"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "path": filename,
        "content": rule_xml
    }
    response = requests.put(url, json=payload, headers=headers, verify=False)
    response.raise_for_status()
    print(f"Rule uploaded successfully to {filename}")
    return response.json()


def fetch_wazuh_logs(limit=50):
    indexer_username = "admin"
    indexer_password = "PASSWORD"
    
    url = f"{WAZUH_INDEXER_URL}/wazuh-alerts*/_search"
    headers = {
        "Content-Type": "application/json"
    }
    query = {
        "size": limit,
        "sort": [
            {"timestamp": {"order": "desc"}}
        ]
    }
    response = requests.get(
        url, headers=headers, json=query, verify=False,
        auth=HTTPBasicAuth(indexer_username, indexer_password)
    )
    response.raise_for_status()
    data = response.json()
    logs = []
    for hit in data.get("hits", {}).get("hits", []):
        source = hit.get("_source", {})
        log_line = source.get("full_log") or str(source)
        logs.append(log_line)
    return '\n'.join(logs)
