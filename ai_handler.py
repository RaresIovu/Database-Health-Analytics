import os
from google.genai import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(api_key = os.getenv("API_KEY"))

def generate_answer(data):
    try:
        prompt = f"Analyze the following metrics and provide only 3 sentences insights, no text formatting, keep it concise: {data}"
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return response.text.strip()
    except Exception as e:
        return {"error": str(e)}