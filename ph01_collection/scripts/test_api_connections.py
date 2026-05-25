import os
from dotenv import load_dotenv
import requests
from typing import Dict, Any

# Load .env
load_dotenv()

AQICN_TOKEN = os.getenv("AQICN_TOKEN")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")
OPENAQ_KEY = os.getenv("OPENAQ_KEY")


def test_openaq_api() -> Dict[str, Any]:
    """Test OpenAQ API v3"""
    try:
        url = "https://api.openaq.org/v3/locations"
        params = {
            "limit": 1,
            "country": "VN"
        }
        headers = {
            "X-API-Key": OPENAQ_KEY
        }
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return {"status": "✅ OK", "data": response.json()}
    except Exception as e:
        return {"status": "❌ FAILED", "error": str(e)}


def test_openweather_api() -> Dict[str, Any]:
    """Test OpenWeather One Call 3.0 API"""
    try:
        # Hà Nội
        lat, lon = 21.0285, 105.8535
        url = "https://api.openweathermap.org/data/3.0/onecall"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_KEY,
            "units": "metric"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return {"status": "✅ OK", "data": response.json()}
    except Exception as e:
        return {"status": "❌ FAILED", "error": str(e)}


def test_aqicn_api() -> Dict[str, Any]:
    """Test AQICN API"""
    try:
        url = "https://api.waqi.info/feed/hanoi/?token=" + AQICN_TOKEN
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "ok":
            return {"status": "✅ OK", "data": data}
        else:
            return {"status": "❌ API Error", "error": data.get("data")}
    except Exception as e:
        return {"status": "❌ FAILED", "error": str(e)}


if __name__ == "__main__":
    print("=" * 60)
    print("TEST KẾT NỐI APIs")
    print("=" * 60)
    
    print("\n1️⃣  Testing OpenAQ API v3...")
    result = test_openaq_api()
    print(f"   {result['status']}")
    if "error" in result:
        print(f"   Error: {result['error']}")
    
    print("\n2️⃣  Testing OpenWeather One Call 3.0...")
    result = test_openweather_api()
    print(f"   {result['status']}")
    if "error" in result:
        print(f"   Error: {result['error']}")
    
    print("\n3️⃣  Testing AQICN API...")
    result = test_aqicn_api()
    print(f"   {result['status']}")
    if "error" in result:
        print(f"   Error: {result['error']}")
    
    print("\n" + "=" * 60)
    print("Nếu tất cả 3 đều ✅ OK, bạn có thể bắt đầu download dữ liệu")
    print("=" * 60)
