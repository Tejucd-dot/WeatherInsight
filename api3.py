import requests
from bs4 import BeautifulSoup

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
weather_tag = soup.find("div", class_="bk-focus__qlook").find("p")
condition = weather_tag.text.strip() if weather_tag else "N/A"


# Extract humidity
details_table = soup.find("table", class_="table table--left table--inner-borders-rows")
humidity = "N/A"
if details_table:
    rows = details_table.find_all("tr")
    
    for row in rows:
        if "Humidity" in row.text:
            
            humidity = row.find_all("td")[0].text.strip()
            
# Print results
print(f"🌡 Temperature: {temperature}")
print(f"⛅ Condition: {condition}")
print(f"💧 Humidity: {humidity}")
