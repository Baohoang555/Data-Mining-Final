import pandas as pd
import requests
from pathlib import Path

BASE_DIR     = Path(__file__).parent.parent.parent
STATIONS_CSV = BASE_DIR / "config" / "stations.csv"

stations = pd.read_csv(STATIONS_CSV)

# Lấy 1 station Hà Nội (HN_001)
station = stations[stations["city"] == "Hà Nội"].iloc[0]
print(f"Testing station: {station['station_id']} - {station['name']}")

lat = station["lat"]
lon = station["lon"]

DATE_FROM = "2019-01-01"
DATE_TO   = "2019-01-31"

url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude":   lat,
    "longitude":  lon,
    "start_date": DATE_FROM,
    "end_date":   DATE_TO,
    "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    "timezone": "Asia/Ho_Chi_Minh",
}

r = requests.get(url, params=params, timeout=60)
print("Status:", r.status_code)
data = r.json()

hourly = data.get("hourly", {})
times  = hourly.get("time", [])
temps  = hourly.get("temperature_2m", [])

print("Total points:", len(times))
print("First 3 timestamps:", times[:3])
print("Last 3 timestamps:", times[-3:])
print("Temp sample:", temps[:3])