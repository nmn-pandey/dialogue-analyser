import requests

url = 'http://127.0.0.1:5001/upload'  # or 'https://127.0.0.1:5001/api' if using HTTPS
headers = {"Content-Type": "multipart/form-data"}

# For text file
text_file_path = "uploads/conversation.txt"
with open(text_file_path, "r", encoding="utf-8") as file:
    text_content = file.read()

files = {
    "file": (text_file_path, text_content, "text/plain"),
}
data = {
    "file_type": "text",
    "api_type": "whisperx",
}

response = requests.post(url, headers=headers, files=files, data=data)
print(f"Response status code: {response.status_code}")
print(f"Response content: {response.content}")

# response = requests.post(url, headers=headers, files=files)
# insights = response.json()
# print(insights)