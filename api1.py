import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
import time
import tkinter as tk
from io import BytesIO

def get_dublin_weather():
    url = "https://www.timeanddate.com/weather/ireland/dublin"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Temperature
    temp_tag = soup.find("div", class_="h2")
    temperature = temp_tag.text.strip() if temp_tag else "N/A"

    # Weather Condition
    weather_tag = soup.find("div", class_="bk-focus__qlook").find("p")
    condition = weather_tag.text.strip() if weather_tag else "N/A"

    img_tag = soup.find("img", {"id":"cur-weather" ,"src": lambda x: x and x.startswith("//c.tadst.com/gfx/w/svg/")})
    print("-------------", img_tag)
    image_url = "https:" + img_tag["src"] if img_tag else "N/A"
    print("sssssssssssssss", image_url)


    # Humidity
    humidity = "N/A"
    table = soup.find("table", class_="table table--left table--inner-borders-rows")
    if table:
        for row in table.find_all("tr"):
            if "Humidity" in row.text:
                humidity = row.find_all("td")[0].text.strip()
                # humidity = row.find_all("td")
                print(humidity,"ssssssssssssssssssssss")

    return temperature, condition, humidity, image_url

def display_weather():
    
    console = Console()
    temp, cond, hum, image_url = get_dublin_weather()
    print(temp)
    print(cond)
    print(hum)
    while True:
        

        table = Table(title="🌍 Dublin Live Weather", style="cyan")

        table.add_column("Metric", style="magenta")
        table.add_column("Value", style="green")

        table.add_row("🌡 Temperature", temp)
        table.add_row("⛅ Condition", cond)
        table.add_row("💧 Humidity", hum)

        console.clear()
        console.print(table)

        time.sleep(300)  # Refresh every 5 minutes
        
    if img_url:
        img_data = requests.get(img_url).content
        img = Image.open(BytesIO(img_data))
        img = img.resize((80, 80))  # Resize icon
        icon = ImageTk.PhotoImage(img)
        icon_label.config(image=icon)
        icon_label.image = icon  # Keep reference

# GUI setup
root = tk.Tk()
root.title("🌤 Dublin Live Weather")
root.geometry("300x250")

temp_label = tk.Label(root, text="", font=("Arial", 14))
temp_label.pack(pady=10)

cond_label = tk.Label(root, text="", font=("Arial", 12))
cond_label.pack()

hum_label = tk.Label(root, text="", font=("Arial", 12))
hum_label.pack()

icon_label = tk.Label(root)
icon_label.pack(pady=10)

refresh_button = tk.Button(root, text="Refresh", command=display_weather)
refresh_button.pack()

# Run the dashboard
display_weather()
root.mainloop()