# PH-01: Data Collection

Module thu thập dữ liệu chất lượng không khí (AQI) và thời tiết cho 3 thành phố Việt Nam: **Hà Nội**, **TP.HCM**, **Đà Nẵng**.

---

## Cấu trúc thư mục

```
ph01_collection/
├── scripts/
│   ├── generate_stations.py     # Bước 1: Tạo danh sách trạm từ OpenAQ API
│   ├── crawl_aqi.py             # Bước 2: Crawl dữ liệu AQI (OpenAQ v3)
│   ├── crawl_weather.py         # Bước 3: Crawl dữ liệu thời tiết (Open-Meteo)
│   ├── build_datalake.py        # Bước 4: Build Data Lake (Parquet)
│   └── test_api_connections.py  # Kiểm tra API keys
│
config/
└── stations.csv                 # Danh sách 54 trạm đo (auto-generated)

data/
├── raw/
│   ├── aqi/
│   │   ├── HN_001/
│   │   │   └── 2024-01-01_2024-01-31.json
│   │   ├── HCM_001/
│   │   │   └── ...
│   │   └── summary_*.csv
│   └── weather/
│       └── weather_summary_*.csv
└── datalake/
    ├── aqi/
    │   ├── city=Hà Nội/year=2024/month=1/*.parquet
    │   └── city=TP.HCM/year=2024/month=1/*.parquet
    └── weather/
        ├── city=Hà Nội/year=2026/month=4/*.parquet
        └── city=TP.HCM/year=2026/month=4/*.parquet
```

---

## Cài đặt

### 1. Tạo virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac
```

### 2. Cài dependencies

```bash
pip install -r requirements.txt
```

### 3. Tạo file `.env`

Tạo file `.env` ở thư mục gốc project:

```env
OPENAQ_KEY=your_openaq_key_here
OPENWEATHER_KEY=your_openweather_key_here
AQICN_TOKEN=your_aqicn_token_here
```

> Đăng ký OpenAQ key miễn phí tại: https://explore.openaq.org/register

---

## Thứ tự chạy

Chạy **đúng thứ tự** các bước sau:

### Bước 0 — Kiểm tra API keys

```bash
python ph01_collection/scripts/test_api_connections.py
```

Kết quả mong đợi: tất cả API đều `✅ OK`.

---

### Bước 1 — Generate danh sách trạm

```bash
python ph01_collection/scripts/generate_stations.py
```

**Kết quả:** tạo file `config/stations.csv` với 54 trạm ở Hà Nội và TP.HCM.

```
city
Hà Nội    43
TP.HCM    11
```

> **Lưu ý:** Script tự động lấy danh sách trạm từ OpenAQ API, không hardcode.

---

### Bước 2 — Crawl dữ liệu AQI

```bash
python ph01_collection/scripts/crawl_aqi.py
```

**Kết quả:** ~139,000 records, lưu vào `data/raw/aqi/`.

```
✅ Total records : 139,367
⚠️  Errors       : 0 stations
📊 Parameters   : pm25, pm10, no2, o3, so2, co, pm1, temperature, relativehumidity, um003
📊 Cities       : {'Hà Nội': 124,667, 'TP.HCM': 14,700}
```

> **Tuỳ chỉnh date range:** Mở file `crawl_aqi.py`, sửa 2 dòng:
> ```python
> DATE_FROM = "2018-01-01"   # Ngày bắt đầu
> DATE_TO   = "2024-12-31"   # Ngày kết thúc
> ```

---

### Bước 3 — Crawl dữ liệu thời tiết

```bash
python ph01_collection/scripts/crawl_weather.py
```

**Kết quả:** ~40,000 records, lưu vào `data/raw/weather/`.

```
✅ Downloaded 40,176 weather records
📊 Temperature range: 19.4°C to 39.4°C
📊 Humidity range: 25% to 100%
```

---

### Bước 4 — Build Data Lake

```bash
python ph01_collection/scripts/build_datalake.py
```

**Kết quả:** Gộp toàn bộ raw data → Parquet partitioned tại `data/datalake/`.

```
✅ AQI Data Lake    : 139,367 records → data/datalake/aqi/
✅ Weather Data Lake: 40,176 records  → data/datalake/weather/
```

---

## Đọc dữ liệu từ Data Lake

Sau khi build xong, các phase khác đọc data như sau:

```python
import pandas as pd

# Đọc toàn bộ AQI
aqi_df = pd.read_parquet("data/datalake/aqi/")

# Đọc AQI theo city + năm cụ thể
aqi_hn_2024 = pd.read_parquet("data/datalake/aqi/city=Hà Nội/year=2024/")

# Đọc Weather
weather_df = pd.read_parquet("data/datalake/weather/")
```

---

## Data Dictionary

### AQI Dataset

| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `station_id` | string | Mã trạm (HN_001, HCM_001...) |
| `name` | string | Tên trạm |
| `city` | string | Thành phố |
| `lat` / `lon` | float | Tọa độ |
| `timestamp` | datetime (UTC) | Thời gian đo |
| `parameter` | string | Chỉ tiêu (pm25, pm10, no2...) |
| `value` | float | Giá trị đo |
| `unit` | string | Đơn vị (µg/m³, ppm...) |
| `year` / `month` | int | Partition key |

### Weather Dataset

| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `station_id` | string | Mã trạm |
| `timestamp` | datetime (UTC) | Thời gian quan sát |
| `temp` | float | Nhiệt độ (°C) |
| `humidity` | int | Độ ẩm (%) |
| `wind_speed` | float | Tốc độ gió (m/s) |
| `pressure` | int | Áp suất (hPa) |
| `description` | string | Mô tả thời tiết |
| `year` / `month` | int | Partition key |

---

## Nguồn dữ liệu

| Nguồn | API | Key cần | Ghi chú |
|-------|-----|---------|---------|
| OpenAQ v3 | `api.openaq.org/v3` | `OPENAQ_KEY` | AQI lịch sử, miễn phí |
| Open-Meteo | `open-meteo.com` | Không cần | Thời tiết, 30 ngày gần nhất (free) |
| OpenWeather | `openweathermap.org` | `OPENWEATHER_KEY` | Backup thời tiết |
