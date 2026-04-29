import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")
AQI_KEY = os.getenv("AQI_API_KEY")

def get_aqi_status(aqi):
    if aqi <= 50:
        return "Good 😊", "Air is clean — great time to be outside!"
    elif aqi <= 100:
        return "Moderate 😐", "Acceptable air quality. Sensitive groups take care."
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups ⚠️", "Reduce prolonged outdoor activity."
    elif aqi <= 200:
        return "Unhealthy 🚨", "Avoid outdoor activity. Keep windows closed."
    else:
        return "Very Unhealthy ☠️", "Stay indoors. Serious health risk."

def get_temp_feel(temp):
    if temp >= 40:
        return "🔥 Extremely hot — stay hydrated!"
    elif temp >= 30:
        return "☀️ Hot day — limit outdoor exposure."
    elif temp >= 20:
        return "🌤️ Pleasant temperature."
    elif temp >= 10:
        return "🧥 Cool — carry a jacket."
    else:
        return "🥶 Cold — dress warmly."

def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": WEATHER_KEY, "units": "metric"}
    res = requests.get(url, params=params)
    data = res.json()

    if res.status_code != 200:
        print(f"❌ Weather error: {data.get('message')}")
        return

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    description = data["weather"][0]["description"].capitalize()

    print(f"\n{'='*45}")
    print(f"  📍 Weather in {city.upper()}")
    print(f"{'='*45}")
    print(f"  🌡️  Temperature : {temp}°C")
    print(f"  💧 Humidity    : {humidity}%")
    print(f"  💨 Wind Speed  : {wind} m/s")
    print(f"  🌥️  Condition   : {description}")
    print(f"\n  💡 Insight     : {get_temp_feel(temp)}")

def fetch_aqi(city):
    url = f"https://api.waqi.info/feed/{city}/"
    params = {"token": AQI_KEY}
    res = requests.get(url, params=params)
    data = res.json()

    if data["status"] != "ok":
        print(f"❌ AQI error: {data.get('data')}")
        return

    aqi = data["data"]["aqi"]
    status, insight = get_aqi_status(aqi)

    print(f"\n{'='*45}")
    print(f"  🌫️  Air Quality in {city.upper()}")
    print(f"{'='*45}")
    print(f"  📊 AQI Score   : {aqi}")
    print(f"  🏷️  Status      : {status}")
    print(f"\n  💡 Insight     : {insight}")
    print(f"{'='*45}\n")

if __name__ == "__main__":
    city = input("Enter city name: ")
    fetch_weather(city)
    fetch_aqi(city)