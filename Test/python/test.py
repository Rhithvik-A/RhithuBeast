import requests
from bs4 import BeautifulSoup

url = "https://www.cricbuzz.com"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    score = soup.find('div', class_ = 'cb-col-100 cb-col cb-col-scores')
    print(score.text, "\n")

soup = BeautifulSoup(response.text, "html.parser")

# Cricbuzz home match cards use this:
cards = soup.find_all("div", class_="cb-mtch-crd")

results = []

for card in cards[:3]:
    text = card.get_text(" ", strip=True)
    results.append(text)
print(results)
