from fastapi import FastAPI
from google import genai
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

# Allow frontend (HTML) to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key="AIzaSyCLEZkSqwjB3xx7-Eq6NKYO4XfYstnkxX8")

def chat_with_retry(prompt, retries=3, delay=0):
    for i in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except genai.errors.ServerError as e:
            print(f"Server busy, retrying in {delay} seconds... ({i+1}/{retries})")
            time.sleep(delay)
    return "Sorry, the server is overloaded. Please try again later."

@app.get("/", tags=["demo"])
def root():
    return "Welcome to my GPT API!!👋"

@app.get("/get-title")
def get_title():
    return chat_with_retry("https://mail.google.com/mail/u/0/#inbox/FMfcgzQcpdrwhftDbvmcjcwVbRqVnwJM is this a safe website just tell the answer only only")

