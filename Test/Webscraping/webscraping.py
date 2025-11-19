import requests
from bs4 import BeautifulSoup
import time

url = "https://www.cricbuzz.com/"
headers = {
    "User-Agent": "Mozilla/5.0"
}

while True:
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        scores = soup.find_all('div', class_='bg-white px-4 pb-2')[:3]

        print("\n=== LIVE UPDATE ===")
        for s in scores:
            print(s.text.strip())
            print("---------------")

    # refresh every 10 seconds
    time.sleep(10)
