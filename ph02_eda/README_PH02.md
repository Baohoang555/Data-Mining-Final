# PH-02: Exploratory Data Analysis (EDA)

Module phân tích khám phá dữ liệu chất lượng không khí — đọc trực tiếp từ Data Lake đã build ở PH-01.

---

## Cấu trúc thư mục

```
ph02_eda/
├── scripts/
│   └── eda_analysis.py       # Script EDA chính
└── outputs/                  # Kết quả tự động tạo khi chạy
    ├── 01_descriptive_stats.png
    ├── 02_map_Hà_Nội.html
    ├── 02_map_TP_HCM.html
    ├── 03_correlation_matrices.png
    ├── 04_time_series_decomposition.png
    ├── 05_fft_frequency_analysis.png
    ├── 06_morans_i_scatter.png
    └── eda_full_report.html
```

---

## Yêu cầu

### Chạy PH-01 trước

PH-02 đọc data từ `data/datalake/` — phải chạy đủ 4 bước PH-01 trước:

```
data/datalake/aqi/      ← bắt buộc có
data/datalake/weather/  ← bắt buộc có
config/stations.csv     ← bắt buộc có
```

### Cài thêm thư viện

```bash
pip install esda libpysal ydata-profiling
```

> Nếu `ydata-profiling` lỗi khi cài, thử: `pip install ydata-profiling --no-deps`

---

## Chạy EDA

```bash
python ph02_eda/scripts/eda_analysis.py
```

Thời gian chạy ước tính: **3–10 phút** (tuỳ kích thước data, phần `ydata-profiling` lâu nhất).

---

## Kết quả output

Script tự động tạo 8 file trong `ph02_eda/outputs/`:

### 1. `01_descriptive_stats.png`
Ba biểu đồ thống kê mô tả:
- Histogram phân phối PM2.5
- Boxplot PM2.5 theo từng thành phố
- Biểu đồ số lượng records theo parameter

### 2. `02_map_Hà_Nội.html` & `02_map_TP_HCM.html`
Bản đồ tương tác (Folium):
- Vị trí các trạm đo (markers đỏ)
- Heatmap mật độ trạm
- Click vào marker để xem tên trạm, số records

> Mở bằng trình duyệt để xem.

### 3. `03_correlation_matrices.png`
Ma trận tương quan giữa các chỉ tiêu ô nhiễm (pm25, pm10, no2, o3, so2, co):
- **Pearson**: tương quan tuyến tính
- **Spearman**: tương quan thứ hạng (robust với outlier)

### 4. `04_time_series_decomposition.png`
Phân tích chuỗi thời gian PM2.5 theo phương pháp **STL Decomposition**:
- **Trend**: xu hướng dài hạn
- **Seasonal**: chu kỳ mùa vụ
- **Residual**: nhiễu ngẫu nhiên

### 5. `05_fft_frequency_analysis.png`
Phân tích tần số (FFT) — xác định chu kỳ lặp lại của PM2.5 (ngày/tuần/năm).

### 6. `06_morans_i_scatter.png`
**Moran's I** — đo mức độ phân cụm không gian của PM2.5:
- `I > 0`: các trạm gần nhau có PM2.5 tương đồng (clustering)
- `I < 0`: các trạm gần nhau có PM2.5 trái chiều (dispersion)
- `p < 0.05`: kết quả có ý nghĩa thống kê

### 7. `eda_full_report.html`
Báo cáo EDA tự động đầy đủ (ydata-profiling):
- Thống kê tổng quan từng cột
- Phân phối dữ liệu
- Missing values
- Correlation matrix

> Mở bằng trình duyệt để xem.

---

## Giải thích kết quả mẫu

```
📊 AQI : 139,367 records | 47 stations
         2016-01-30 → 2026-03-30

📈 ADF Test (Stationarity):
   ADF Statistic : -8.4231
   p-value       : 0.0000
   ✅ Stationary (p < 0.05)

📐 Moran's I Results:
   I statistic : 0.3412
   p-value     : 0.0100
   ✅ Spatial CLUSTERING (p < 0.05)
```

| Chỉ số | Ý nghĩa |
|--------|---------|
| ADF p < 0.05 | Chuỗi thời gian dừng → phù hợp cho mô hình dự báo |
| Moran's I > 0 | Các trạm gần nhau có mức ô nhiễm tương đồng |
| Pearson PM2.5-PM10 cao | PM2.5 và PM10 cùng nguồn phát sinh |

---

## Tuỳ chỉnh

### Đổi parameter phân tích

Mặc định script phân tích **PM2.5**. Để đổi sang parameter khác, sửa trong `eda_analysis.py`:

```python
# Tìm và đổi "pm25" thành parameter muốn phân tích
aqi_df[aqi_df["parameter"] == "pm25"]   # → đổi "pm25" thành "no2", "pm10"...
```

### Đổi tần suất resample time series

```python
# Mặc định: Daily ("D")
.resample("D")["value"].mean()

# Đổi thành weekly:
.resample("W")["value"].mean()

# Đổi thành monthly:
.resample("ME")["value"].mean()
```

---

## Lưu ý kỹ thuật

- Script **sample 5,000 records** khi tạo ydata-profiling report (tránh quá chậm). Tăng con số này nếu cần báo cáo đầy đủ hơn.
- Moran's I cần `k=4` nearest neighbors — nếu số station < 5 sẽ tự adjust.
- STL cần tối thiểu **60 điểm dữ liệu** — nếu thiếu, bước này sẽ bị skip.
- Tất cả timestamp đều chuẩn hoá về **UTC**.
