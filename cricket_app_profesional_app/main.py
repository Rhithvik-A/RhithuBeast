from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

URL = "https://www.cricbuzz.com/cricket-match/live-scores"
HEADERS = {"User-Agent": "Mozilla/5.0"}

@app.get("/scores")
def get_scores():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    blocks = soup.find_all("div", class_="cb-mtch-lst")[:3]

    scores = []

    for b in blocks:
        text = b.get_text(separator="\n", strip=True)
        scores.append(text)
    print(scores)
    return "Hi"
    
