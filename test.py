import requests

url = "http://localhost:5000/chat"
data = { "message": "Buyer" }

response = requests.post(url, json=data)
print("Status Code:", response.status_code)
print("Bot Reply:", response.json())
