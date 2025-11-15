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
    matches = soup.findAll('a', class_='h-full block w-[316px]')[:3]
    print(matches [0])

    
else:
    print(f"Failed to fetch page. Status code: {response.status_code}")
