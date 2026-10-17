import requests

url = "https://www.fifa.com/en/match-centre?liveNow=true&date=2026-07-15"
response = requests.get(url)

print(response.text)