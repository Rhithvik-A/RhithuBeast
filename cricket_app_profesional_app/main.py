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

url = "https://www.cricbuzz.com"
headers = {
    "User-Agent": "Mozilla/5.0"
}

@app.get("/scores")
def scores():
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"scores": ["Error loading data"]}

    soup = BeautifulSoup(response.text, "html.parser")

    score_blocks = soup.find_all('div', class_='bg-white px-4 pb-2')[:3]

    scores_list = []

    for block in score_blocks:
        html_block = str(block)
        html_block = html_block.replace(
            'bg-white px-4 pb-2',
            'bg-gray-800 text-gray-300 min-h-[60px]'
        )
        scores_list.append(html_block)

    return {"scores": scores_list}

