import requests
import json

# Webhook API URL (adjust if running on a different host)
webhook_url = "https://nerdshub.ai/api/webhook/"

# Load the saved encrypted payload
def load_encrypted_payload(filename="encrypted_payload.json"):
    with open(filename, "r") as file:
        return json.load(file)

# Load encrypted data
encrypted_payload = load_encrypted_payload()

# Send a POST request to the webhook
try:
    response = requests.post(webhook_url, json=encrypted_payload, verify=False)  # ⚠️ verify=False for SSL warnings
    print("📩 Server Response:", response.json())
except requests.exceptions.RequestException as e:
    print(f"❌ Error sending request: {e}")
