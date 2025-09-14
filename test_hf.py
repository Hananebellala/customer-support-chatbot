import requests, os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
print("Token starts with:", HF_TOKEN[:10])  # just to confirm it's loaded

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"  # open free model
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

response = requests.post(API_URL, headers=headers, json={"inputs": "Hello, how are you?"})
print(response.status_code)
print(response.json())
