"""
Crawl Weather data từ Open-Meteo Archive API
Miễn phí, không cần API key
Historical weather theo khoảng thời gian cố định
"""

import json
import time
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
print("CRAWL WEATHER DATA - Open-Meteo Archive API (Historical)")
print("=" * 70)

# Chỉnh khoảng thời gian ở đây
START_DATE = "2024-12-31"
END_DATE   = "2025-12-31"


@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def fetch_weather_data(lat: float, lon: float, start_date: str, end_date: str) -> dict:
    """
    Fetch historical weather từ Open-Meteo Archive API
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
        "timezone": "UTC"
    }
    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()
    return response.json()


print(f"\n📅 Date range: {START_DATE} to {END_DATE}")
print(f"📍 Stations: {len(STATIONS)}")
print(f"\n📥 Downloading weather data...\n")

all_weather = []
error_count = 0

for idx, row in tqdm(list(STATIONS.iterrows()), desc="Stations"):
    station_id = row["station_id"]
    lat = row["lat"]
    lon = row["lon"]
    city = row["city"]
    name = row.get("name", station_id)

    try:
        data = fetch_weather_data(lat, lon, START_DATE, END_DATE)

        # Save raw JSON theo từng station
        station_dir = RAW_DATA_DIR / station_id
        station_dir.mkdir(parents=True, exist_ok=True)

        file_path = station_dir / f"{START_DATE}_{END_DATE}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Parse hourly data
        if "hourly" in data:
            hourly = data["hourly"]
            timestamps = hourly.get("time", [])
            temps = hourly.get("temperature_2m", [])
            humidity = hourly.get("relative_humidity_2m", [])
            wind_speed = hourly.get("wind_speed_10m", [])
            weather_code = hourly.get("weather_code", [])

            for ts, temp, hum, wind, wcode in zip(
                timestamps, temps, humidity, wind_speed, weather_code
            ):
                all_weather.append({
                    "station_id": station_id,
                    "name": name,
                    "city": city,
                    "lat": lat,
                    "lon": lon,
                    "timestamp": ts,
                    "temperature": temp,
                    "humidity": hum,
                    "wind_speed": wind,
                    "weather_code": wcode,
                })

        # nghỉ nhẹ tránh gọi dồn
        time.sleep(0.3)

    except Exception as e:
        error_count += 1
        tqdm.write(f"❌ Error {station_id}: {str(e)[:80]}")

print(f"\n✅ Downloaded {len(all_weather)} weather records")
print(f"⚠️  Errors: {error_count} stations")

# Summary
if all_weather:
    df = pd.DataFrame(all_weather)

    print(f"\n📊 Weather data summary:")
    print(f"   Total records: {len(df):,}")
    print(f"   Stations: {df['station_id'].nunique()}")
    print(f"   Cities: {df['city'].value_counts().to_dict()}")
    print(f"   Temperature range: {df['temperature'].min():.1f}°C to {df['temperature'].max():.1f}°C")
    print(f"   Humidity range: {df['humidity'].min():.0f}% to {df['humidity'].max():.0f}%")
    print(f"   Wind speed range: {df['wind_speed'].min():.1f} to {df['wind_speed'].max():.1f} m/s")

    # Save summary CSV
    summary_file = RAW_DATA_DIR / f"weather_summary_{START_DATE}_{END_DATE}.csv"
    df.to_csv(summary_file, index=False)
    print(f"\n💾 Saved summary: {summary_file}")
else:
    print("⚠️  No weather data found")

print("\n" + "=" * 70)