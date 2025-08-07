import requests
from bs4 import BeautifulSoup
import time

def get_dublin_weather():
    url = "https://www.timeanddate.com/weather/ireland/dublin"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract temperature
    temp_tag = soup.find("div", class_="h2")
    temperature = temp_tag.text.strip() if temp_tag else "N/A"

    # Extract weather condition
    condition_tag = soup.find("div", class_="small")
    condition = condition_tag.text.strip() if condition_tag else "N/A"

    # Extract humidity
    humidity = "N/A"
    table = soup.find("table", class_="table table--left table--inner-borders-rows")
    if table:
        for row in table.find_all("tr"):
            if "Humidity" in row.text:
                humidity = row.find_all("td")[1].text.strip()

    return temperature, condition, humidity

while True:
    temp, cond, hum = get_dublin_weather()
    print("------ Dublin Weather ------")
    print(f"Temperature: {temp}")
    print(f"Condition: {cond}")
    print(f"Humidity: {hum}")
    print("----------------------------\n")

    time.sleep(300)  # Refresh every 5 minutes
