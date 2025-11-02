from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key="AIzaSyDw-Y9MILuDzngEbeCItnqV9NAiqsof3x0")

@app.get("/ai_response")
def ai_response(Question: str = Query(..., description="Your question")):
    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=Question
            )
            return {"answer": response.text}
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)
    return {"error": "Failed to get response after retries."}
