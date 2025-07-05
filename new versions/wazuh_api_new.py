import requests
import urllib3
from config import WAZUH_URL, WAZUH_USER, WAZUH_PASS

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # annoying warning, ignore

def wazuh_authenticate():
    # quick login, gets bearer token
    url = f"{WAZUH_URL}/security/user/authenticate"
    try:
        r = requests.post(url, json={"username": WAZUH_USER, "password": WAZUH_PASS}, verify=False)
        r.raise_for_status()
        d = r.json()
        return d["data"]["token"] if "data" in d and "token" in d["data"] else None
    except Exception as e:
        print("wazuh_authenticate failed:", e)
        return None

def upload_wazuh_rule(rule_xml, token):
    # uploads rule xml, not much validation
    url = f"{WAZUH_URL}/ruleset/rules?pretty=true"
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/xml"}
    try:
        r = requests.post(url, data=rule_xml.encode('utf-8'), headers=headers, verify=False)
        r.raise_for_status()
        return r.json()  # might want to check success/failure
    except Exception as e:
        print("upload_wazuh_rule error:", e)
        return {}

def fetch_wazuh_logs(token, limit=50):
    # grabs latest logs, returns as one big string (TODO: paginate)
    url = f"{WAZUH_URL}/security/events?limit={limit}&sort=desc"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.get(url, headers=headers, verify=False)
        resp.raise_for_status()
        items = resp.json().get("data", {}).get("affected_items", [])
        # some logs might not have full_log, quick skip
        logs = []
        for event in items:
            logline = event.get("full_log")
            if logline:
                logs.append(logline)
        return '\n'.join(logs)
    except Exception as err:
        print("fetch_wazuh_logs error:", err)
        return ""

# # Quick test:
# t = wazuh_authenticate()
# if t:
#     print(fetch_wazuh_logs(t))
