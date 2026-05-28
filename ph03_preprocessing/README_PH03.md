# PH-03: Data Preprocessing & Feature Engineering — An

Module này xử lý phần **PH-03** cho đề tài mới **AirGlobal: Khai phá dữ liệu và dự báo chất lượng không khí toàn cầu 2014–2025**.

## Mục tiêu

PH-03 biến dữ liệu Kaggle/raw hoặc datalake của Thọ thành dataset sạch để PH-05 train mô hình classification.

Các bước chính:

1. Đọc dữ liệu từ:
   - `data/datalake/aqi/**/*.parquet` nếu máy có `pyarrow` hoặc `fastparquet`
   - fallback sang `data/raw/global_air_quality_2014_2025.csv`
2. Chuẩn hóa schema:
   - `PM2.5 (ug/m3)` → `pm25`
   - `PM10 (ug/m3)` → `pm10`
   - `AQI_Bucket` → `aqi_bucket`
   - `Wind_Speed (km/h)` → `wind_speed`
3. Chuẩn hóa target `target_aqi_bucket` từ `AQI_Bucket`.
4. Tránh leakage:
   - không dùng `AQI` numeric làm feature để dự đoán `AQI_Bucket`
   - không dùng `AQI_Bucket` gốc làm feature
5. Xử lý dữ liệu:
   - drop duplicate theo `country/state/city/date`
   - xử lý giá trị ngoài giới hạn vật lý
   - IQR clipping / winsorization theo country
   - hierarchical median imputation: city → country → global
6. Feature engineering:
   - time features: `year`, `month`, `quarter`, `season`, `month_sin`, `month_cos`
   - pollutant ratios: `pm25_pm10_ratio`, `no2_nox_ratio`, `so2_no2_ratio`
   - environment interactions: `pm25_humidity_interaction`, `pm25_wind_dispersion`
   - geography frequency encoding: `country_freq`, `city_freq`, `country_city_freq`
   - lag/rolling theo chuỗi thời gian của từng `country + city`: lag 1/3/12 period, rolling mean/std 3/6/12 period
7. Chia train/validation/test theo thời gian để giảm data leakage.

## Cách chạy

Từ thư mục gốc project:

```bash
python ph03_preprocessing/scripts/preprocess_airglobal.py
```

## Output

Sau khi chạy xong, thư mục `ph03_preprocessing/outputs/` có:

| File | Ý nghĩa |
|---|---|
| `processed_airglobal_features.pkl` | Dataset sạch full cho PH-05, lưu nhanh hơn CSV |
| `processed_airglobal_sample_5000.csv` | Sample nhỏ để xem nhanh |
| `missing_report_before_imputation.csv` | Thống kê missing trước xử lý |
| `physical_invalid_values_report.csv` | Giá trị ngoài giới hạn vật lý |
| `outlier_iqr_report.csv` | Số outlier bị clip bằng IQR |
| `feature_catalog.csv` | Danh sách feature, type, group |
| `label_distribution.csv` | Phân phối nhãn AQI sau chuẩn hóa |
| `split_summary.csv` | Số dòng train/val/test |
| `preprocessing_metadata.json` | Metadata tổng hợp |

## Lưu ý khi báo cáo

Điểm quan trọng nhất là **tránh data leakage**. Vì `AQI_Bucket` thường được tạo từ `AQI`, PH-03 vẫn giữ `AQI` để EDA/báo cáo nhưng PH-05 sẽ loại `AQI` khỏi feature list.

Câu thuyết trình gợi ý:

> Ở phần tiền xử lý, em chuẩn hóa dữ liệu AirGlobal từ Kaggle, xử lý missing values, outliers và tạo các feature theo thời gian, ô nhiễm, môi trường và địa lý. Đặc biệt, em loại bỏ `AQI` khỏi input của mô hình khi target là `AQI_Bucket` để tránh data leakage. Dataset sau xử lý được chia train/validation/test theo thời gian để mô phỏng bài toán dự báo trên dữ liệu tương lai.
