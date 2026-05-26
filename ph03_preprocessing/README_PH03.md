# PH-03: Tiền xử lý dữ liệu & Feature Engineering — An

Module này hoàn thành phần PH-03 theo phân công của An: xử lý missing values, outlier, tạo đặc trưng lag/rolling/time/spatial, tạo nhãn classification và chia tập train/validation/test để PH-05 dùng trực tiếp.

## Cách chạy

```bash
# Từ thư mục gốc project
python ph03_preprocessing/scripts/preprocess_features.py
```

## Input

Script tự đọc theo thứ tự ưu tiên:

1. `data/datalake/aqi/` và `data/datalake/weather/` nếu môi trường có `pyarrow` hoặc `fastparquet`.
2. Fallback sang `data/raw/aqi/summary_*.csv` và `data/raw/weather/weather_summary_*.csv` nếu chưa đọc được Parquet.

## Output chính

| File | Ý nghĩa |
|---|---|
| `ph03_preprocessing/outputs/processed_aqi_features.csv` | Dataset đã làm sạch + feature engineering, dùng cho PH-05 |
| `missing_pattern_report.csv` | Tỷ lệ missing và nhận định MCAR/MAR/MNAR-like |
| `outlier_report.csv` | Số outlier IQR, số điểm bị xem là sensor error, số điểm giữ lại như sự kiện ô nhiễm thật |
| `imputation_summary.csv` | Tóm tắt interpolation và bước xử lý gap dài |
| `feature_catalog.csv` | Danh sách feature numeric được dùng cho mô hình |
| `split_summary.csv` | Số dòng train/validation/test |
| `preprocessing_metadata.json` | Metadata, label mapping, split strategy, ghi chú chất lượng dữ liệu |

## Phương pháp đã triển khai

- **Missing values**: phân tích missing theo feature, trạm và giờ; nội suy tuyến tính theo từng trạm với `limit=2` để xử lý gap dưới 3 giờ. Với gap dài, script dùng `KNNImputer` khi data đủ nhỏ; với data nhiều năm, fallback sang median theo `station_id × hour`, sau đó `city × hour`, cuối cùng global median để tránh runtime quá lâu trên laptop.
- **Outlier**: áp dụng IQR 1.5× theo từng `station_id × month`. Điểm quá ngưỡng vật lý hoặc spike cô lập so với rolling median được xem là lỗi sensor và chuyển thành missing; điểm IQR còn lại được giữ như sự kiện ô nhiễm nặng thật.
- **Feature engineering**: tạo lag 1h/3h/6h/12h/24h; rolling mean/std/max/min 3h/6h/24h; số giờ PM2.5 vượt ngưỡng trong 24h; sin/cos cho hour/day/month; `is_rush_hour`, `is_weekend`, `is_dry_season`; khoảng cách Haversine tới khu công nghiệp và đường trục lớn gần nhất.
- **Target**: `target_aqi_label_next_1h`, dự báo nhãn AQI của giờ kế tiếp từ PM2.5, tránh leakage so với dùng nhãn hiện tại.
- **Split**: test set là 15% timestamp cuối cùng theo thời gian; train/validation được chia stratified trên phần còn lại.

## Ghi chú quan trọng

Trong dữ liệu Thọ gửi, AQI và Weather không overlap timestamp, nên weather feature bị impute fallback. Muốn kết quả mô hình tốt hơn, nên crawl lại weather cùng khoảng thời gian với AQI.
