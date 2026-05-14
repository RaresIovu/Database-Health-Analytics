import os
from google.genai import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(api_key = os.getenv("API_KEY")) # Api key needs to be defined in .env

def generate_answer(data):
    try:
        prompt = f"Analyze the following metrics and provide only 3 sentences insights, no text formatting, keep it concise: {data}" # Concise summary to be displayed in frontend
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return response.text.strip() # We only need the text component of the response(the response also contains data such as token usage etc)
    except Exception:
        return "Analysis temporarily unavailable. The AI engine is experiencing high traffic. Metrics are still being recorded." # I chose to format it so that we dont get a traceback or giant text wall in frontend