import requests
import time
from config import CALDERA_URL, CALDERA_API_KEY, CALDERA_AGENT_GROUP

def launch_attack(plan_name="atomic_attack"):
    # Launches a caldera attack, returns adventure id. 
    url = f"{CALDERA_URL}/api/v2/adventures"
    data = {"adversary_id": plan_name, "group": CALDERA_AGENT_GROUP}
    headers = {"KEY": CALDERA_API_KEY, "Content-Type": "application/json"}
    try:
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
    except Exception as e:
        print(f"launch_attack failed: {e}")
        return None
    d = resp.json()
    # Sometimes 'id' might not be present, need to check
    return d.get("id", None)

def wait_for_attack_completion(adventure_id):
    # Poll until the adventure finishes. TODO: add timeout
    url = f"{CALDERA_URL}/api/v2/adventures/{adventure_id}"
    headers = {"KEY": CALDERA_API_KEY}
    while True:
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            data = r.json()
            state = data.get("state")
        except Exception as err:
            print("Polling error:", err)
            time.sleep(5)
            continue
        # Print state for debugging
        print("Caldera state:", state)
        if state == "finished":
            break
        time.sleep(7)  # Not sure if 10s is best, try 7s for fun

# Example usage:
# ai
