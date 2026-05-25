"""
Crawl AQI measurements từ OpenAQ API v3
Đúng endpoint: /v3/sensors/{sensor_id}/hours (daily average)
"""

import os
import json
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed
from tqdm import tqdm

load_dotenv()

OPENAQ_KEY   = os.getenv("OPENAQ_KEY")
BASE_DIR     = Path(__file__).parent.parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw" / "aqi"
STATIONS_CSV = BASE_DIR / "config" / "stations.csv"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("CRAWL AQI MEASUREMENTS - OpenAQ API v3 (sensor-based)")
print("=" * 70)

if not STATIONS_CSV.exists():
    print("❌ Chưa có stations.csv, chạy generate_stations.py trước")
    exit(1)

stations = pd.read_csv(STATIONS_CSV)
print(f"\n📍 Loaded {len(stations)} stations")

# Date range — test 1 tháng trước, sau đó mở rộng
DATE_FROM = "2024-01-01"
DATE_TO   = "2024-01-31"


@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def fetch_sensors(openaq_id: int) -> list:
    """Lấy danh sách sensors của 1 location."""
    url = f"https://api.openaq.org/v3/locations/{openaq_id}/sensors"
    r = requests.get(url, headers={"X-API-Key": OPENAQ_KEY}, timeout=30)
    r.raise_for_status()
    return r.json().get("results", [])


@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def fetch_sensor_hours(sensor_id: int, date_from: str, date_to: str) -> list:
    """Lấy hourly averages từ 1 sensor."""
    url = f"https://api.openaq.org/v3/sensors/{sensor_id}/hours"
    params = {
        "limit":      1000,
        "date_from":  f"{date_from}T00:00:00Z",
        "date_to":    f"{date_to}T23:59:59Z",
    }
    r = requests.get(url, params=params, headers={"X-API-Key": OPENAQ_KEY}, timeout=30)
    r.raise_for_status()
    return r.json().get("results", [])


print(f"\n📅 Date range: {DATE_FROM} → {DATE_TO}")
print(f"📥 Crawling...\n")

all_records = []
error_count = 0

for _, station in tqdm(stations.iterrows(), total=len(stations), desc="Stations"):
    station_id = station["station_id"]
    openaq_id  = int(station["openaq_id"])
    name       = station["name"]
    city       = station["city"]

    try:
        # Bước 1: lấy sensors của location
        sensors = fetch_sensors(openaq_id)
        if not sensors:
            tqdm.write(f"⚠️  {station_id}: no sensors")
            continue

        station_records = []

        # Bước 2: fetch measurements từng sensor
        for sensor in sensors:
            sensor_id = sensor.get("id")
            param     = sensor.get("parameter", {}).get("name", "unknown")

            try:
                results = fetch_sensor_hours(sensor_id, DATE_FROM, DATE_TO)
                for rec in results:
                    station_records.append({
                        "station_id": station_id,
                        "name":       name,
                        "city":       city,
                        "lat":        station["lat"],
                        "lon":        station["lon"],
                        "timestamp":  rec.get("period", {}).get("datetimeTo", {}).get("utc"),
                        "parameter":  param,
                        "value":      rec.get("value"),
                        "unit":       sensor.get("parameter", {}).get("units", ""),
                    })
            except Exception as e:
                tqdm.write(f"⚠️  {station_id} sensor {sensor_id}: {str(e)[:50]}")

        # Save raw JSON per station
        if station_records:
            out_dir = RAW_DATA_DIR / station_id
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / f"{DATE_FROM}_{DATE_TO}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(station_records, f, ensure_ascii=False)
            all_records.extend(station_records)

    except Exception as e:
        error_count += 1
        tqdm.write(f"❌ {station_id}: {str(e)[:60]}")

# Summary
print(f"\n{'='*70}")
print(f"✅ Total records : {len(all_records)}")
print(f"⚠️  Errors       : {error_count} stations")

if all_records:
    df = pd.DataFrame(all_records)
    print(f"\n📊 Parameters   : {df['parameter'].unique()}")
    print(f"📊 Cities       : {df['city'].value_counts().to_dict()}")
    summary = RAW_DATA_DIR / f"summary_{DATE_FROM}_{DATE_TO}.csv"
    df.to_csv(summary, index=False)
    print(f"💾 Saved        : {summary}")

print("=" * 70)