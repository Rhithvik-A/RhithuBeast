import time
from google import genai

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

print(chat_with_retry("who is the prime minister of india"))
