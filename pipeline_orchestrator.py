from ollama_api import generate_wazuh_rule
from wazuh_api import wazuh_authenticate, upload_wazuh_rule, fetch_wazuh_logs
from caldera_api import launch_attack, wait_for_attack_completion

def pipeline_loop(nl_attack, caldera_attack_id="atomic_attack", cycles=5):
    print("Authenticating to Wazuh...")
    token = wazuh_authenticate()

    # Step 1: Generate initial rule from NL description
    print("Generating initial rule via LLM...")
    rule_xml = generate_wazuh_rule(nl_attack=nl_attack)
    print("Generated rule:", rule_xml[:300], '...')
    print("Uploading rule to Wazuh...")
    upload_wazuh_rule(rule_xml)

    for cycle in range(1, cycles + 1):
        print(f"\n--- Cycle {cycle} ---")
        print("Launching Caldera attack...")
        adv_id = launch_attack(plan_name=caldera_attack_id)
        print("Waiting for attack to complete...")
        wait_for_attack_completion(adv_id)
        print("Fetching logs from Wazuh...")
        logs = fetch_wazuh_logs(token, limit=50)
        print("Generating new rule via LLM from logs...")
        rule_xml = generate_wazuh_rule(logs=logs)
        print("Uploading rule to Wazuh...")
        upload_wazuh_rule(rule_xml)

    print("Pipeline completed.")

if __name__ == "__main__":
    # Example NL attack input
    nl_attack = "Simulate credential dumping attack using mimikatz and detect suspicious LSASS access."
    pipeline_loop(nl_attack, caldera_attack_id="atomic_attack", cycles=5)
