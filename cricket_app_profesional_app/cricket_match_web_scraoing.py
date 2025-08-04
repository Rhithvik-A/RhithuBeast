import requests
from bs4 import BeautifulSoup

url = "https://www.cricbuzz.com/"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # First 3 matches
    score = soup.findAll('li', class_ = 'cb-view-all-ga cb-match-card cb-bg-white')
    score = score[:3]
    # Finding a tag so that 'shedule, table ' will not be vesible
    for i in score:
        score = i.find('a')
        if score:
            print(score.text, "\n")
            pass
        else:
            print("Live score section not found.")
else:
    print(f"Failed to fetch page. Status code: {response.status_code}")