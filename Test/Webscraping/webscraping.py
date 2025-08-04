import requests
from bs4 import BeautifulSoup

url = "https://www.cricbuzz.com/live-cricket-scores/128809/hun-vs-rom-2nd-match-budapest-cup-2025"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    score = soup.find('div', class_ = 'cb-col-100 cb-col cb-col-scores')
    print(score.text, "\n")
