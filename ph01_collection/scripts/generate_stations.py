"""
Generate stations.csv từ OpenAQ API data (Auto-generated, không hardcode)
Lọc chỉ stations ở Việt Nam
"""

import os
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed

load_dotenv()

OPENAQ_KEY  = os.getenv("OPENAQ_KEY")
BASE_DIR    = Path(__file__).parent.parent.parent
OUTPUT_FILE = BASE_DIR / "config" / "stations.csv"

print("=" * 70)
print("GENERATE stations.csv từ OpenAQ API (Auto-generate from API)")
print("=" * 70)


def _guess_city(lat, lon):
    """Đoán thành phố dựa vào tọa độ bounding box."""
    if lat is None or lon is None:
        return "Unknown"
    if 20.5 <= lat <= 21.5 and 105.5 <= lon <= 106.2:
        return "Hà Nội"
    if 10.4 <= lat <= 11.2 and 106.3 <= lon <= 107.0:
        return "TP.HCM"
    if 15.8 <= lat <= 16.3 and 107.9 <= lon <= 108.5:
        return "Đà Nẵng"
    return "Other_VN"


@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def fetch_openaq_locations():
    """Fetch tất cả locations Việt Nam từ OpenAQ API v3."""
    url     = "https://api.openaq.org/v3/locations"
    params  = {"limit": 1000, "countries_id": 56}
    headers = {"X-API-Key": OPENAQ_KEY}
    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


# Download locations
print("\n📥 Fetching VN locations from OpenAQ API...")
try:
    data = fetch_openaq_locations()
    print("✅ Got response from OpenAQ")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Parse locations
stations = []
if "results" in data:
    results = data["results"]
    print(f"📊 Total locations: {len(results)}")

    for loc in results:
        name = loc.get("name", "Unknown")
        lat  = loc.get("coordinates", {}).get("latitude")
        lon  = loc.get("coordinates", {}).get("longitude")

        # Thử nhiều field city theo thứ tự ưu tiên
        city = (
            loc.get("locality")
            or loc.get("municipality")
            or loc.get("city")
            or _guess_city(lat, lon)
        )

        # Nếu city vẫn trống sau các field trên, dùng guess
        if not city or city in ("Unknown", "N/A"):
            city = _guess_city(lat, lon)

        if lat is not None and lon is not None:
            stations.append({
                "station_id": None,
                "name":       name,
                "lat":        lat,
                "lon":        lon,
                "city":       city,
                "openaq_id":  loc.get("id"),
                "source":     "OpenAQ API"
            })

# Tạo DataFrame
if stations:
    df = pd.DataFrame(stations)

    # Loại bỏ duplicates theo tọa độ
    df = df.drop_duplicates(subset=["lat", "lon"])

    # Normalize tên city
    city_map = {
        "Hanoi":            "Hà Nội",
        "Ha Noi":           "Hà Nội",
        "Ho Chi Minh City": "TP.HCM",
        "Ho Chi Minh":      "TP.HCM",
        "N/A":              "Other_VN",
    }
    df["city"] = df["city"].replace(city_map)

    # Sort by city, name
    df = df.sort_values(["city", "name"]).reset_index(drop=True)

    # Gán station_id theo city prefix
    city_prefix = {
        "Hà Nội":   "HN",
        "TP.HCM":   "HCM",
        "Đà Nẵng":  "DN",
        "Other_VN": "VN",
    }
    city_counter = {}
    for idx, row in df.iterrows():
        prefix = city_prefix.get(row["city"], "VN")
        city_counter[prefix] = city_counter.get(prefix, 0) + 1
        df.at[idx, "station_id"] = f"{prefix}_{city_counter[prefix]:03d}"

    print(f"\n✅ Extracted {len(df)} stations from OpenAQ")
    print(f"\n📍 Breakdown by city:")
    print(df["city"].value_counts())

    # Tạo thư mục config nếu chưa có
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Save
    output_cols = ["station_id", "name", "lat", "lon", "city", "openaq_id", "source"]
    df[output_cols].to_csv(OUTPUT_FILE, index=False)

    print(f"\n✅ Saved to: {OUTPUT_FILE}")
    print(f"\n📝 Sample rows:")
    print(df[output_cols].head(10).to_string(index=False))

else:
    print("❌ No stations found")
    exit(1)

print("\n" + "=" * 70)