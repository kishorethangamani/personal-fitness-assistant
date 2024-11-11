from langflow.load import run_flow_from_json
from dotenv import load_dotenv
import requests
import json
from typing import Optional
import os


BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "a013eeda-6028-40a5-a300-85872f02ee12"
#APPLICATION_TOKEN = os.getenv("LANGFLOW_TOKEN")
APPLICATION_TOKEN = "AstraCS:XZqZtgqFijbRDHqkbkdxjtJC:c4543ffeb8a45c1932c16e54c23f92249bce295b9c3cada0a153705286b1269f"
load_dotenv()

def dict_to_string(obj, level=0):
    strings = []
    indent = "  " * level  # Indentation for nested levels
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                nested_string = dict_to_string(value, level + 1)
                strings.append(f"{indent}{key}: {nested_string}")
            else:
                strings.append(f"{indent}{key}: {value}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            nested_string = dict_to_string(item, level + 1)
            strings.append(f"{indent}Item {idx + 1}: {nested_string}")
    else:
        strings.append(f"{indent}{obj}")

    return ", ".join(strings)


def genai(profile, question):
    TWEAKS = {
        "TextInput-0zRsg": {
            "input_value": question
        },
        "TextInput-NsFq9": {
            "input_value": dict_to_string(profile)
        },
    }

    result = run_flow_from_json(flow="GenAIfyp.json",
                                input_value="message",
                                fallback_to_env_vars=True,
                                tweaks=TWEAKS)

    return result[0].outputs[0].results["text"].data["text"]

# Note: Replace **<YOUR_APPLICATION_TOKEN>** with your actual Application token
# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}


def get_macros(profile, goals):
    TWEAKS = {
       "TextInput-JOZXD": {
            "input_value": ", ".join(goals)
        },
        "TextInput-hs8H9": {
            "input_value": dict_to_string(profile)
        }
    }
    return run_flow("", tweaks=TWEAKS, application_token=APPLICATION_TOKEN)
    
    
def run_flow(message: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  application_token: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.
    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/macros"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    
    return json.loads(response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"])