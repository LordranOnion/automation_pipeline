import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_wazuh_rule(nl_attack=None, logs=None):
    # TODO: maybe add support for both at once? not sure if needed
    if not nl_attack and not logs:
        raise Exception("need either nl_attack or logs")

    # Just reuse var for prompt, keep it simple
    if nl_attack:
        p = "Given this scenario, write a Wazuh XML rule:\n" + nl_attack
    else:
        p = "Given these Wazuh logs, write a detection rule in XML:\n" + logs

    try:
        # Not sure if gpt-4.1 is always available, fallback if needed
        resp = openai.ChatCompletion.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a SIEM rule engineer."},
                {"role": "user", "content": p}
            ],
            max_tokens=800
        )
    except Exception as e:
        print("LLM API error:", e)
        return ""

    # Sometimes content isn't present? Should check
    choices = resp.get("choices", [])
    if not choices or "message" not in choices[0]:
        print("no choices or message in response")
        return ""
    rule_xml = choices[0]["message"].get("content", "")
    # In real use might want to validate XML, skip for now
    return rule_xml.strip() if rule_xml else ""

# quick test:
# print(generate_wazuh_rule(nl_attack="Some attack desc"))
