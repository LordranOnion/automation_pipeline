# wazuh_api.py
import requests
import urllib3
from config import WAZUH_URL, WAZUH_USER, WAZUH_PASS

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def wazuh_authenticate():
    url = f"{WAZUH_URL}/security/user/authenticate"
    response = requests.post(url, json={"username": WAZUH_USER, "password": WAZUH_PASS}, verify=False)
    response.raise_for_status()
    return response.json()["data"]["token"]

def upload_wazuh_rule(rule_xml, token):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/xml"}
    url = f"{WAZUH_URL}/ruleset/rules?pretty=true"
    response = requests.post(url, data=rule_xml.encode('utf-8'), headers=headers, verify=False)
    response.raise_for_status()
    return response.json()

def fetch_wazuh_logs(token, limit=50):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{WAZUH_URL}/security/events?limit={limit}&sort=desc"
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    logs = [event["full_log"] for event in response.json()["data"]["affected_items"]]
    return '\n'.join(logs)
