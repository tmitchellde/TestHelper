import pyautogui
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class Grabber:
    def __init__(self, api_key):
        """
        Initialize the Grabber class with the ChatGPT API key.
        """
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/chat/completions"

    def capture_screenshot(self, filename="screenshot.png"):
        """
        Capture a screenshot and save it to the specified file path.
        """
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        return filename

    def send_prompt_to_chatgpt(self, prompt):
        """
        Send a text prompt to the ChatGPT API and return the response.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4",  # Use the desired GPT model
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500
        }

        response = requests.post(self.api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def process_response(self, response):
        """
        Process the ChatGPT response to determine question type and answer.
        """
        if "multiple-choice" in response.lower():
            return "letter", response.split()[-1]  # Example logic for parsing answer
        elif "programming" in response.lower():
            return "code", response
        else:
            return None, "Unrecognized question type"

    def send_email(self, to_email, subject, body, from_email="your_email@example.com", from_password="your_password"):
        """
        Send an email with the specified details.
        """
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(from_email, from_password)
                server.send_message(msg)
            print(f"Email sent to {to_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def cleanup(self, file_path):
        """
        Delete the specified file if it exists.
        """
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {file_path} deleted.")
