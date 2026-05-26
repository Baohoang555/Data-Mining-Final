# Báo cáo PH-03 — Tiền xử lý dữ liệu

## 1. Mục tiêu

PH-03 chuẩn bị dữ liệu sạch và bộ đặc trưng đầu vào cho bài toán phân lớp mức độ ô nhiễm. Dữ liệu đầu vào gồm AQI/pollutants theo trạm và dữ liệu thời tiết theo giờ. Output của phase này là bảng feature theo từng `station_id × timestamp`, target dự báo nhãn AQI giờ kế tiếp và split train/validation/test.

## 2. Kết quả xử lý dữ liệu

- AQI loaded: **139,023 records**.
- Weather loaded: **40,176 records**.
- Hourly station matrix: **85,102 rows**.
- Rows sau khi tạo target next 1h: **85,055 rows**.
- Số trạm: **47**.
- Khoảng thời gian: **2016-01-30 01:00:00+00:00 → 2026-03-30 04:00:00+00:00**.
- Số feature numeric đưa vào mô hình: **155**.

## 3. Missing values

Script phân tích missing theo từng feature, theo trạm và theo giờ để đưa ra nhận định MCAR/MAR/MNAR-like. Với dữ liệu hiện tại, weather feature bị missing 100% sau khi merge vì file weather không overlap timestamp với AQI. Các feature `pm1` và `um003` missing khoảng 96.08%, chủ yếu phụ thuộc trạm đo nên được ghi nhận dạng MAR/MNAR-like.

Cách xử lý:

1. Nội suy tuyến tính theo từng trạm với `limit=2`, tương ứng xử lý gap nhỏ dưới 3 giờ.
2. Với gap dài, dùng `KNNImputer` khi data nhỏ; với dataset nhiều năm, dùng median theo station-hour/city-hour để tránh thời gian chạy quá lâu.
3. Nếu một cột vẫn missing toàn bộ, dùng fallback median hoặc 0 và ghi chú trong metadata.

## 4. Outlier

Outlier được phát hiện bằng IQR 1.5× theo từng `station_id × month` để tránh trộn mùa và trạm. Điểm vượt ngưỡng vật lý hoặc spike cô lập so với rolling median được xem là lỗi cảm biến; outlier còn lại được giữ vì có thể phản ánh ngày ô nhiễm thật.

Một số kết quả chính:

| Feature | IQR outliers | Sensor errors set NaN | Kept as real pollution |
|---|---:|---:|---:|
| pm25 | 1,037 | 354 | 683 |
| pm10 | 817 | 299 | 518 |
| no2 | 1,040 | 389 | 651 |
| co | 1,361 | 713 | 648 |

## 5. Feature engineering

Các nhóm feature đã tạo:

- Lag features: 1h, 3h, 6h, 12h, 24h cho pollutant và weather.
- Rolling features: mean/std/max/min với window 3h, 6h, 24h.
- Threshold feature: số giờ PM2.5 vượt ngưỡng Moderate trong 24h trước.
- Time encoding: sin/cos cho giờ, ngày trong tuần, tháng.
- Binary features: `is_rush_hour`, `is_weekend`, `is_dry_season`.
- Spatial features: khoảng cách Haversine đến khu công nghiệp và đường trục lớn gần nhất.

## 6. Target và split

Target chính là `target_aqi_label_next_1h`, tức nhãn AQI của giờ kế tiếp. Cách này phù hợp với mục tiêu dự báo và giảm nguy cơ data leakage.

Phân phối nhãn:

| Label | Count |
|---|---:|
| Moderate | 43,949 |
| Unhealthy | 22,990 |
| Very_Unhealthy | 12,242 |
| Good | 5,617 |
| Hazardous | 257 |

Split:

| Split | Rows |
|---|---:|
| Train | 66,187 |
| Validation | 14,184 |
| Test | 4,684 |

Test set lấy 15% timestamp cuối cùng để mô phỏng dự báo tương lai; train/validation chia stratified trên phần còn lại.

## 7. Hạn chế và đề xuất

Weather hiện không overlap với AQI nên cần crawl lại weather cùng khoảng thời gian AQI. Nhãn `Hazardous` rất ít, cần dùng class weight, SMOTEENN hoặc thu thập thêm dữ liệu sự kiện ô nhiễm cao để cải thiện recall của lớp hiếm.
