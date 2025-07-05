from chatgpt_api_new import generate_wazuh_rule
from wazuh_api_new import wazuh_authenticate, upload_wazuh_rule, fetch_wazuh_logs
from caldera_api_new import launch_attack, wait_for_attack_completion

def pipeline_loop(nl_attack, caldera_attack_id="atomic_attack", cycles=5):
    # quick script for SIEM-auto pipeline
    token = wazuh_authenticate()  # just call login
    rule_xml = generate_wazuh_rule(nl_attack=nl_attack)
    upload_wazuh_rule(rule_xml, token)

    for c in range(cycles):
        print(f"cycle {c+1}")
        adv_id = launch_attack(plan_name=caldera_attack_id)
        wait_for_attack_completion(adv_id)
        # fetch logs and send to ChatGPT
        logs = fetch_wazuh_logs(token)
        # sometimes chatgpt gives weird stuff, quick fix:
        try:
            rule_xml = generate_wazuh_rule(logs=logs)
        except Exception as e:
            print("rule gen fail", e)
            continue
        upload_wazuh_rule(rule_xml, token)
        #print("Uploaded rule:", rule_xml[:100]) # debug

    print("done.")

if __name__ == "__main__":
    attack = "Simulate credential dumping with mimikatz."
    pipeline_loop(attack, cycles=3)  # just a couple cycles for test
