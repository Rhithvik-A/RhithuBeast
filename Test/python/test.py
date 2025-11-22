import requests
from bs4 import BeautifulSoup

url = "https://www.cricbuzz.com"
headers = {
    "User-Agent": "Mozilla/5.0"
}
def a ():
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            score = soup.find('div', class_ = 'flex flex-col gap-3 mb-2 pt-4')
            return(score)
        




