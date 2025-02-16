# Function to fetch data from API
import requests

def fetch_attachment_data(api_url, files):
    try:
        response = requests.post(api_url, files=files)
        response.raise_for_status()  # Ensure response is valid (200 OK)
        data = response.json()[0].get('content', "Attachment content is not found.")
        return data
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def fetch_data(api_url, payload):
    try:
        response = requests.post(api_url, json=payload)
        data = response.json().get('text', "No response received.")
        return data
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"