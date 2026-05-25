"""
Crawl Weather data từ Open-Meteo API (Free, Historical support)
Không cần API key
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import requests
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_fixed
from tqdm import tqdm

BASE_DIR = Path(__file__).parent.parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw" / "weather"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Load stations từ config
STATIONS = pd.read_csv(BASE_DIR / "config" / "stations.csv")

print("=" * 70)
print("CRAWL WEATHER DATA - Open-Meteo API (Free, Historical)")
print("=" * 70)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def fetch_weather_data(lat: float, lon: float, start_date: str, end_date: str) -> dict:
    """
    Fetch historical weather từ Open-Meteo API (Free, unlimited)
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
        "timezone": "Asia/Ho_Chi_Minh"
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

# Download 30 ngày gần nhất
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

start_str = start_date.strftime("%Y-%m-%d")
end_str = end_date.strftime("%Y-%m-%d")

print(f"\n📅 Date range: {start_str} to {end_str}")
print(f"📍 Stations: {len(STATIONS)}")
print(f"\n📥 Downloading weather data...\n")

all_weather = []
error_count = 0

for idx, row in tqdm(list(STATIONS.iterrows()), desc="Stations"):
    station_id = row["station_id"]
    lat = row["lat"]
    lon = row["lon"]
    city = row["city"]
    
    try:
        data = fetch_weather_data(lat, lon, start_str, end_str)
        
        # Save raw JSON
        file_path = RAW_DATA_DIR / f"{station_id}_{start_str}_{end_str}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Parse hourly data
        if "hourly" in data:
            hourly = data["hourly"]
            timestamps = hourly.get("time", [])
            temps = hourly.get("temperature_2m", [])
            humidity = hourly.get("relative_humidity_2m", [])
            wind_speed = hourly.get("wind_speed_10m", [])
            
            for ts, temp, hum, wind in zip(timestamps, temps, humidity, wind_speed):
                all_weather.append({
                    "station_id": station_id,
                    "city": city,
                    "lat": lat,
                    "lon": lon,
                    "timestamp": ts,
                    "temperature": temp,
                    "humidity": hum,
                    "wind_speed": wind,
                })
    
    except Exception as e:
        error_count += 1
        tqdm.write(f"❌ Error {station_id}: {str(e)[:50]}")

print(f"\n✅ Downloaded {len(all_weather)} weather records")
print(f"⚠️  Errors: {error_count} stations")

# Summary
if all_weather:
    df = pd.DataFrame(all_weather)
    print(f"\n📊 Weather data summary:")
    print(f"   Total records: {len(df)}")
    print(f"   Stations: {df['station_id'].nunique()}")
    print(f"   Temperature range: {df['temperature'].min():.1f}°C to {df['temperature'].max():.1f}°C")
    print(f"   Humidity range: {df['humidity'].min():.0f}% to {df['humidity'].max():.0f}%")
    print(f"   Wind speed range: {df['wind_speed'].min():.1f} to {df['wind_speed'].max():.1f} m/s")
    
    # Save summary CSV
    summary_file = RAW_DATA_DIR / f"weather_summary_{start_str}_{end_str}.csv"
    df.to_csv(summary_file, index=False)
    print(f"\n💾 Saved summary: {summary_file}")
else:
    print("⚠️  No weather data found")

print("\n" + "=" * 70)
