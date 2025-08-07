from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_dublin_weather():
    url = "https://www.timeanddate.com/weather/ireland/dublin"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    temp_tag = soup.find("div", class_="h2")
    temperature = temp_tag.text.strip() if temp_tag else "N/A"

    cond_tag = soup.find("div", class_="bk-focus__qlook").find("p")
    condition = cond_tag.text.strip() if cond_tag else "N/A"

    humidity = "N/A"
    table = soup.find("table", class_="table table--left table--inner-borders-rows")
    if table:
        for row in table.find_all("tr"):
            if "Humidity" in row.text:
                humidity = row.find_all("td")[0].text.strip()

    #img_tag = soup.find("img", {"src": lambda x: x and x.startswith("/weather/i/")})
    #img_url = "https://www.timeanddate.com" + img_tag["src"] if img_tag else None
    img_tag = soup.find("img", {"id":"cur-weather" ,"src": lambda x: x and x.startswith("//c.tadst.com/gfx/w/svg/")})
    print("-------------", img_tag)
    image_url = "https:" + img_tag["src"] if img_tag else "N/A"
    print("sssssssssssssss", image_url)


    return temperature, condition, humidity, image_url

@app.route('/')
def index():
    temp, cond, hum, img_url = get_dublin_weather()
    return render_template('index.html', temp=temp, cond=cond, hum=hum, img_url=img_url)

if __name__ == '__main__':
    app.run(debug=True)
