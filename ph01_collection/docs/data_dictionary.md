# Data Dictionary

## AQI Dataset

| Thuộc tính | Kiểu dữ liệu | Mô tả | Nguồn |
|-----------|-----------|-------|-------|
| station_id | string | Mã trạm đo (ví dụ: HN_001, HCM_003) | stations.csv |
| name | string | Tên trạm đo | stations.csv |
| city | string | Thành phố (Hà Nội, TP.HCM, Đà Nẵng) | stations.csv |
| lat | float | Vĩ độ | stations.csv |
| lon | float | Kinh độ | stations.csv |
| timestamp | datetime | Thời gian lấy mẫu (UTC) | OpenAQ API |
| parameter | string | Chỉ tiêu ô nhiễm (PM2.5, PM10, O3, NO2, SO2, CO, etc.) | OpenAQ API |
| value | float | Giá trị chỉ tiêu | OpenAQ API |
| unit | string | Đơn vị đo (µg/m³, ppb, ppm) | OpenAQ API |
| year | int | Năm (2018-2024) | Computed |
| month | int | Tháng (1-12) | Computed |

**Phân vùng Parquet**: `datalake/aqi/city={city}/year={year}/month={month}/*.parquet`

---

## Weather Dataset

| Thuộc tính | Kiểu dữ liệu | Mô tả | Nguồn |
|-----------|-----------|-------|-------|
| station_id | string | Mã trạm đo | stations.csv |
| name | string | Tên trạm đo | stations.csv |
| city | string | Thành phố | stations.csv |
| lat | float | Vĩ độ | stations.csv |
| lon | float | Kinh độ | stations.csv |
| timestamp | datetime | Thời gian quan sát | OpenWeather API |
| temp | float | Nhiệt độ (°C) | OpenWeather API |
| feels_like | float | Cảm giác nhiệt độ (°C) | OpenWeather API |
| humidity | int | Độ ẩm (%) | OpenWeather API |
| pressure | int | Áp suất (hPa) | OpenWeather API |
| wind_speed | float | Tốc độ gió (m/s) | OpenWeather API |
| wind_deg | int | Hướng gió (độ, 0-360) | OpenWeather API |
| clouds | int | Độ che phủ mây (%) | OpenWeather API |
| description | string | Mô tả thời tiết (Clear, Cloudy, Rainy, etc.) | OpenWeather API |
| year | int | Năm (2018-2024) | Computed |
| month | int | Tháng (1-12) | Computed |

**Phân vùng Parquet**: `datalake/weather/city={city}/year={year}/month={month}/*.parquet`

---

## Stations Reference

| station_id | name | city | lat | lon |
|-----------|------|------|-----|-----|
| HN_001 | Tây Hồ | Hà Nội | 21.0859 | 105.8581 |
| HN_002 | Ba Đình | Hà Nội | 21.0532 | 105.8395 |
| HN_003 | Hoàn Kiếm | Hà Nội | 21.0285 | 105.8535 |
| HN_004 | Đống Đa | Hà Nội | 21.0331 | 105.8125 |
| HN_005 | Hai Bà Trưng | Hà Nội | 21.0037 | 105.8476 |
| HN_006 | Long Biên | Hà Nội | 21.0469 | 105.8741 |
| HN_007 | Cầu Giấy | Hà Nội | 21.0277 | 105.7894 |
| HCM_001 | Quận 1 | TP.HCM | 10.7769 | 106.7009 |
| HCM_002 | Quận 2 | TP.HCM | 10.8000 | 106.7627 |
| HCM_003 | Quận 3 | TP.HCM | 10.7897 | 106.6882 |
| HCM_004 | Quận 4 | TP.HCM | 10.7604 | 106.6829 |
| HCM_005 | Quận 5 | TP.HCM | 10.7516 | 106.6763 |
| HCM_006 | Quận 6 | TP.HCM | 10.7419 | 106.6545 |
| HCM_007 | Quận 7 | TP.HCM | 10.7465 | 106.7352 |
| DN_001 | Hải Châu | Đà Nẵng | 16.0675 | 108.2105 |
| DN_002 | Thanh Khê | Đà Nẵng | 16.0784 | 108.1975 |
| DN_003 | Sơn Trà | Đà Nẵng | 16.0872 | 108.2301 |
| DN_004 | Ngũ Hành Sơn | Đà Nẵng | 16.0089 | 108.1957 |
| DN_005 | Liên Chiểu | Đà Nẵng | 16.0291 | 108.2412 |
| DN_006 | Cẩm Lệ | Đà Nẵng | 16.0566 | 108.1627 |

**File**: `config/stations.csv`

---

## Tổng cộng 18 thuộc tính chính

**AQI Dataset**: 11 thuộc tính độc lập
- station_id, name, city, lat, lon, timestamp, parameter, value, unit, year, month

**Weather Dataset**: 14 thuộc tính độc lập
- station_id, name, city, lat, lon, timestamp, temp, feels_like, humidity, pressure, wind_speed, wind_deg, clouds, description, year, month

*Lưu ý: Cả 2 datasets đều có các cột chung (station_id, name, city, lat, lon, timestamp, year, month) để dễ dàng join dữ liệu khi phân tích*
