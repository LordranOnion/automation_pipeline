import openai
import os
from config import OPENAI_API_KEY

api_key = os.environ.get("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

def generate_wazuh_rule(nl_attack):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": nl_attack}
        ]
    )
    
    return response.choices[0].message.content