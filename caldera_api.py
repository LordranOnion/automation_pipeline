# caldera_api.py
import requests
from config import CALDERA_URL, CALDERA_API_KEY, CALDERA_AGENT_GROUP

def launch_attack(plan_name="atomic_attack"):
    headers = {
        "Authorization": f"Bearer {CALDERA_API_KEY}",
        "Content-Type": "application/json"
    }
    url = f"{CALDERA_URL}/api/v2/adventures"
    data = {
        "adversary_id": plan_name,
        "group": CALDERA_AGENT_GROUP
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()["id"]


def wait_for_attack_completion(adventure_id):
    headers = {"KEY": CALDERA_API_KEY}
    url = f"{CALDERA_URL}/api/v2/adventures/{adventure_id}"
    import time
    while True:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        status = response.json()["state"]
        if status == "finished":
            break
        time.sleep(10)
