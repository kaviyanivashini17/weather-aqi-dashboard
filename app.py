import requests
import streamlit as st
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

WEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")
AQI_KEY = os.getenv("AQI_API_KEY")

# ── Page config ────────────────────────────────
st.set_page_config(
    page_title="AirWeather — Live Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ── Custom CSS ─────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0f1e;
    color: #e8eaf0;
}

.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1528 50%, #0a1520 100%);
}

h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

/* Hero title */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #60a5fa, #34d399, #60a5fa);
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 4s linear infinite;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}
@keyframes shimmer {
    0%   { background-position: 0% }
    100% { background-position: 200% }
}

.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    color: #6b7a99;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* Card base */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem;
    backdrop-filter: blur(12px);
    transition: border-color 0.2s;
}
.card:hover { border-color: rgba(96,165,250,0.3); }

/* Metric cards */
.metric-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    text-align: center;
}
.metric-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #6b7a99;
    margin-bottom: 0.4rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #e8eaf0;
}
.metric-unit {
    font-size: 0.85rem;
    color: #6b7a99;
}

/* AQI badge */
.aqi-badge {
    display: inline-block;
    padding: 0.35rem 1rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.aqi-good    { background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
.aqi-mod     { background: rgba(251,191,36,0.15);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.aqi-sens    { background: rgba(251,146,60,0.15);  color: #fb923c; border: 1px solid rgba(251,146,60,0.3); }
.aqi-bad     { background: rgba(248,113,113,0.15); color: #f87171; border: 1px solid rgba(248,113,113,0.3); }
.aqi-vbad    { background: rgba(192,38,211,0.15);  color: #e879f9; border: 1px solid rgba(192,38,211,0.3); }

/* Section headers */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #60a5fa;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(96,165,250,0.2);
}

/* Insight box */
.insight-box {
    background: rgba(96,165,250,0.06);
    border-left: 3px solid #60a5fa;
    border-radius: 0 10px 10px 0;
    padding: 0.9rem 1.2rem;
    font-size: 0.92rem;
    color: #a8b4d0;
    margin-top: 0.5rem;
}

/* Best time box */
.best-time-box {
    background: rgba(52,211,153,0.06);
    border: 1px solid rgba(52,211,153,0.2);
    border-radius: 14px;
    padding: 1.3rem 1.5rem;
}
.best-time-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #34d399;
    margin-bottom: 0.5rem;
}
.best-time-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #e8eaf0;
}

/* Forecast bar */
.forecast-bar-wrap { margin-top: 0.4rem; }
.forecast-label {
    font-size: 0.75rem;
    color: #6b7a99;
    margin-bottom: 0.25rem;
}

/* Input + button overrides */
div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.7rem 1rem !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: rgba(96,165,250,0.5) !important;
    box-shadow: 0 0 0 3px rgba(96,165,250,0.1) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────
def get_aqi_info(aqi):
    if aqi <= 50:
        return "Good", "aqi-good", "😊", "#34d399", "Air is clean — great time to go outside!"
    elif aqi <= 100:
        return "Moderate", "aqi-mod", "😐", "#fbbf24", "Acceptable quality. Sensitive groups should be cautious."
    elif aqi <= 150:
        return "Sensitive Groups", "aqi-sens", "⚠️", "#fb923c", "Reduce prolonged outdoor activity."
    elif aqi <= 200:
        return "Unhealthy", "aqi-bad", "🚨", "#f87171", "Avoid outdoor activity. Keep windows closed."
    else:
        return "Very Unhealthy", "aqi-vbad", "☠️", "#e879f9", "Stay indoors. Serious health risk."

def get_temp_insight(temp):
    if temp >= 40:   return "🔥 Extreme heat — stay hydrated and avoid direct sun."
    elif temp >= 33: return "☀️ Hot day — limit prolonged outdoor exposure."
    elif temp >= 24: return "🌤️ Warm and pleasant — good conditions outside."
    elif temp >= 15: return "🌥️ Mild weather — comfortable for most activities."
    elif temp >= 8:  return "🧥 Cool — carry a jacket if heading out."
    else:            return "🥶 Cold — dress in warm layers."

def get_best_time(aqi, temp, wind):
    score = 100
    if aqi > 150:   score -= 50
    elif aqi > 100: score -= 25
    elif aqi > 50:  score -= 10
    if temp > 38:   score -= 20
    elif temp > 33: score -= 10
    if wind > 10:   score -= 10

    if score >= 80:
        return "Morning (6–9 AM)", "Best conditions — cool temp, clean air.", "#34d399"
    elif score >= 60:
        return "Evening (6–8 PM)", "Decent conditions — temperature drops help.", "#fbbf24"
    else:
        return "Stay Indoors", "Current conditions are not ideal for outdoor activity.", "#f87171"

def fetch_weather(city):
    url = "http://api.openweathermap.org/data/2.5/weather"
    res = requests.get(url, params={"q": city, "appid": WEATHER_KEY, "units": "metric"})
    return res.json() if res.status_code == 200 else None

def fetch_forecast(city):
    url = "http://api.openweathermap.org/data/2.5/forecast"
    res = requests.get(url, params={"q": city, "appid": WEATHER_KEY, "units": "metric", "cnt": 40})
    return res.json() if res.status_code == 200 else None

def fetch_aqi(city):
    res = requests.get(f"https://api.waqi.info/feed/{city}/", params={"token": AQI_KEY})
    data = res.json()
    return data["data"] if data["status"] == "ok" else None

def parse_forecast(data):
    daily = {}
    for item in data["list"]:
        date = datetime.fromtimestamp(item["dt"]).strftime("%a %d %b")
        if date not in daily:
            daily[date] = {"temps": [], "icons": [], "desc": []}
        daily[date]["temps"].append(item["main"]["temp"])
        daily[date]["desc"].append(item["weather"][0]["description"])
    result = []
    for date, vals in list(daily.items())[1:6]:
        result.append({
            "date": date,
            "min": round(min(vals["temps"]), 1),
            "max": round(max(vals["temps"]), 1),
            "desc": vals["desc"][0].capitalize()
        })
    return result


# ── Layout ─────────────────────────────────────
st.markdown('<div class="hero-title">AirWeather</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Live Weather & Air Quality Intelligence</div>', unsafe_allow_html=True)

col_input, col_btn = st.columns([4, 1])
with col_input:
    city = st.text_input("", placeholder="Enter city — Bangalore, London, Tokyo...", label_visibility="collapsed")
with col_btn:
    search = st.button("Analyse →")

st.markdown("<br>", unsafe_allow_html=True)

if search and city:
    with st.spinner(""):
        weather  = fetch_weather(city)
        forecast = fetch_forecast(city)
        aqi_data = fetch_aqi(city)

    if not weather:
        st.error("City not found. Please check the spelling.")
        st.stop()

    temp      = weather["main"]["temp"]
    feels     = weather["main"]["feels_like"]
    humidity  = weather["main"]["humidity"]
    wind      = weather["wind"]["speed"]
    condition = weather["weather"][0]["description"].capitalize()
    visibility= weather.get("visibility", 0) // 1000

    # ── Row 1: City + condition ─────────────────
    st.markdown(f"""
    <div class="card" style="margin-bottom:1.2rem">
        <div style="display:flex;justify-content:space-between;align-items:center">
            <div>
                <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:700;color:#e8eaf0">
                    📍 {city.title()}
                </div>
                <div style="color:#6b7a99;font-size:0.9rem;margin-top:0.2rem">
                    {datetime.now().strftime("%A, %d %B %Y · %H:%M")}
                </div>
            </div>
            <div style="text-align:right">
                <div style="font-size:0.85rem;color:#a8b4d0">{condition}</div>
                <div style="font-size:0.78rem;color:#6b7a99;margin-top:0.2rem">Feels like {feels}°C</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Row 2: Weather metrics ──────────────────
    st.markdown('<div class="section-label">⛅ Current Weather</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        (c1, "Temperature",  f"{temp}",      "°C"),
        (c2, "Humidity",     f"{humidity}",  "%"),
        (c3, "Wind Speed",   f"{wind}",      "m/s"),
        (c4, "Visibility",   f"{visibility}", "km"),
    ]
    for col, label, val, unit in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{val}<span class="metric-unit">{unit}</span></div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f'<div class="insight-box">💡 {get_temp_insight(temp)}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 3: AQI + Best Time ──────────────────
    col_aqi, col_best = st.columns([1.4, 1])

    with col_aqi:
        st.markdown('<div class="section-label">🌫️ Air Quality Index</div>', unsafe_allow_html=True)
        if aqi_data:
            aqi = aqi_data["aqi"]
            status, badge_cls, emoji, color, insight = get_aqi_info(aqi)
            bar_pct = min(int((aqi / 300) * 100), 100)
            st.markdown(f"""
            <div class="card">
                <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1rem">
                    <div style="font-family:'Syne',sans-serif;font-size:3rem;font-weight:800;color:{color}">{aqi}</div>
                    <div>
                        <div style="font-size:0.75rem;color:#6b7a99;text-transform:uppercase;letter-spacing:.08em">AQI Score</div>
                        <span class="aqi-badge {badge_cls}">{emoji} {status}</span>
                    </div>
                </div>
                <div style="background:rgba(255,255,255,0.06);border-radius:999px;height:6px;overflow:hidden;margin-bottom:0.9rem">
                    <div style="width:{bar_pct}%;height:100%;background:{color};border-radius:999px;transition:width 1s ease"></div>
                </div>
                <div style="font-size:0.88rem;color:#a8b4d0">{insight}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("AQI data unavailable for this city.")

    with col_best:
        st.markdown('<div class="section-label">🕐 Best Time Outside</div>', unsafe_allow_html=True)
        aqi_val = aqi_data["aqi"] if aqi_data else 100
        time_label, time_desc, time_color = get_best_time(aqi_val, temp, wind)
        st.markdown(f"""
        <div class="best-time-box" style="border-color:rgba(255,255,255,0.1);background:rgba(255,255,255,0.03);height:100%">
            <div class="best-time-title">Recommended Window</div>
            <div class="best-time-value" style="color:{time_color}">{time_label}</div>
            <div style="font-size:0.85rem;color:#6b7a99;margin-top:0.5rem">{time_desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 4: 5-Day Forecast ───────────────────
    if forecast:
        st.markdown('<div class="section-label">📅 5-Day Forecast</div>', unsafe_allow_html=True)
        days = parse_forecast(forecast)
        cols = st.columns(5)
        for i, (col, day) in enumerate(zip(cols, days)):
            temp_range = day["max"] - day["min"]
            bar_fill = min(int((day["max"] / 45) * 100), 100)
            with col:
                st.markdown(f"""
                <div class="metric-card" style="padding:1rem">
                    <div style="font-family:'Syne',sans-serif;font-size:0.75rem;font-weight:700;color:#60a5fa;margin-bottom:0.6rem;text-transform:uppercase;letter-spacing:.06em">{day['date']}</div>
                    <div style="font-size:1.4rem;font-weight:700;color:#e8eaf0;font-family:'Syne',sans-serif">{day['max']}°</div>
                    <div style="font-size:0.8rem;color:#6b7a99;margin-bottom:0.5rem">{day['min']}° low</div>
                    <div style="background:rgba(255,255,255,0.06);border-radius:4px;height:4px;overflow:hidden">
                        <div style="width:{bar_fill}%;height:100%;background:linear-gradient(90deg,#60a5fa,#34d399);border-radius:4px"></div>
                    </div>
                    <div style="font-size:0.72rem;color:#6b7a99;margin-top:0.5rem">{day['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

elif not search:
    st.markdown("""
    <div style="text-align:center;padding:4rem 0;color:#2d3a55">
        <div style="font-size:4rem;margin-bottom:1rem">🌍</div>
        <div style="font-family:'Syne',sans-serif;font-size:1.1rem;color:#3d4f6e">Enter a city above to get started</div>
    </div>
    """, unsafe_allow_html=True)