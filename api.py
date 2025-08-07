import requests
from bs4 import BeautifulSoup

url = "https://www.timeanddate.com/weather/ireland/dublin"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

temp_elem = soup.find("div", class_="h2")
if temp_elem:
    print("🌡️ Current temperature in Dublin:", temp_elem.text.strip())
else:
    print("Temperature not found")