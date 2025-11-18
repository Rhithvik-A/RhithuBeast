import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

URL = "https://www.cricbuzz.com/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

@app.get("/matches")
def get_matches():
    response = requests.get(URL, headers=HEADERS)

    if response.status_code != 200:
        return {"error": "Could not fetch Cricbuzz"}

    soup = BeautifulSoup(response.text, "html.parser")

    # Cricbuzz home match cards use this:
    cards = soup.find_all("div", class_="cb-mtch-crd")

    results = []

    for card in cards[:3]:
        text = card.get_text(" ", strip=True)
        results.append(text)

    return {"matches": results}
