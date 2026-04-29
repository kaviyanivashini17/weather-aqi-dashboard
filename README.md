# weather-aqi-dashboard# 🌍 AirWeather — Live Weather & AQI Dashboard

A professional weather and air quality dashboard built with Python and Streamlit.
Fetches **live data** from real APIs and turns it into actionable insights — not just raw numbers.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red?style=flat-square&logo=streamlit)
![APIs](https://img.shields.io/badge/APIs-OpenWeatherMap%20%7C%20WAQI-green?style=flat-square)

---

## 🔥 Features

- 🌡️ **Live Weather** — Temperature, humidity, wind speed, visibility
- 🌫️ **Air Quality Index (AQI)** — Real-time AQI with color-coded status
- 💡 **Smart Insights** — Human-readable advice, not just numbers
- 🕐 **Best Time Outside** — AI-style recommendation based on AQI + temp + wind
- 📅 **5-Day Forecast** — Daily high/low with visual temperature bars
- 🎨 **Professional Dark UI** — Glassmorphism design with animated elements

---

🚀 **Live Demo** → https://weather-aqi-dashboard-cz2etqprhm4e28wt4lnyki.streamlit.app/

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.10+ |
| UI Framework | Streamlit |
| Weather API | OpenWeatherMap |
| Air Quality API | WAQI (World Air Quality Index) |
| Environment | python-dotenv |

---

## ⚙️ Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/kaviyanivashini17/weather-aqi-dashboard.git
cd weather-aqi-dashboard
```

### 2. Install dependencies
```bash
python -m pip install requests streamlit python-dotenv
```

### 3. Add your API keys
Create a `.env` file in the root folder:
```env
OPENWEATHER_API_KEY=your_openweather_key
AQI_API_KEY=your_waqi_key
```

Get free keys here:
- OpenWeatherMap → https://openweathermap.org/api
- WAQI → https://aqicn.org/data-platform/token

### 4. Run the app
```bash
streamlit run app.py
```

---

## 💡 Key Insights This App Provides

- AQI above 150 → app warns you to stay indoors
- Temperature above 33°C → recommends limiting outdoor time
- Combines AQI + temp + wind to suggest the **best time to go outside**
- 5-day forecast helps plan your week around weather

---

## 📁 Project Structure

weather_aqi_dashboard/
├── app.py          # Streamlit dashboard
├── main.py         # Terminal version
├── .env            # API keys (not uploaded)
├── .gitignore      # Ignores .env
└── README.md       # This file

---

## 🙋 Author

**Kaviyanivashini** — [github.com/kaviyanivashini17](https://github.com/kaviyanivashini17)
