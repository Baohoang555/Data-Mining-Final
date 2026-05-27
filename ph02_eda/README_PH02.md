# PH-02: Exploratory Data Analysis (EDA)

Module phân tích khám phá dữ liệu chất lượng không khí toàn cầu, đọc trực tiếp từ **AQI Data Lake** đã build ở PH-01.

Dữ liệu đầu vào sử dụng bộ **World Air Pollution & AQI Dataset (2014–2025)** đã được chuyển sang Parquet và partition theo `city/year`.

---

## Cấu trúc thư mục

```bash
ph02_eda/
├── scripts/
│   └── eda_analysis.py          # Script EDA chính
└── outputs/                     # Kết quả tạo tự động sau khi chạy
    ├── 01_descriptive_stats.png
    ├── 02_top_polluted_cities.png
    ├── 03_country_city_coverage.png
    ├── 04_correlation_matrices.png
    ├── 05_time_series_decomposition.png
    ├── 06_fft_frequency_analysis.png
    └── 07_vietnam_top_cities.png
```

---

## Dữ liệu đầu vào

PH-02 đọc dữ liệu từ:

```bash
data/datalake/aqi/
```

Cấu trúc datalake:

```bash
data/datalake/aqi/
├── 10th_of_ramadan/
│   ├── 2014/
│   │   └── data.parquet
│   ├── 2015/
│   │   └── data.parquet
│   └── ...
├── ho_chi_minh_city/
│   ├── 2014/
│   │   └── data.parquet
│   └── ...
└── ...
```

Dataset hiện tại đã build thành công với:
- **1,349,280 records**
- **2,271 cities**
- **27,241 parquet files**

---

## Yêu cầu trước khi chạy

### 1. Chạy PH-01 trước

Bắt buộc phải có AQI datalake từ PH-01:

```bash
data/datalake/aqi/
```

### 2. Cài thư viện cần thiết

```bash
pip install pandas pyarrow matplotlib seaborn scipy statsmodels folium
```

Nếu dùng virtual environment:

```bash
.venv\Scripts\activate
```

---

## Cách chạy

Chạy script từ thư mục gốc project:

```bash
python ph02_eda/scripts/eda_analysis.py
```

Thời gian chạy phụ thuộc vào máy và số lượng file parquet, thường mất vài phút vì script sẽ đọc toàn bộ datalake rồi gộp lại để phân tích.

---

## Nội dung phân tích

Script `eda_analysis.py` hiện tại thực hiện các nhóm phân tích sau:

### 1. Load dữ liệu từ datalake
- Đọc toàn bộ file `.parquet` trong `data/datalake/aqi`
- Gộp các partition thành một DataFrame thống nhất
- Chuẩn hoá cột `Date`
- Loại bỏ các record thiếu `Date`, `City`, `Country`, hoặc `AQI`

### 2. Thống kê mô tả
Tạo file:

```bash
01_descriptive_stats.png
```

Bao gồm:
- Histogram phân phối **AQI**
- Histogram phân phối **PM2.5**
- Biểu đồ top 10 quốc gia theo số lượng records

### 3. Thành phố ô nhiễm nhất
Tạo file:

```bash
02_top_polluted_cities.png
```

Phân tích:
- Mean AQI theo từng `Country + City`
- Lọc các thành phố có tối thiểu 30 records
- Xác định top 10 thành phố có AQI trung bình cao nhất

### 4. Mức độ bao phủ dữ liệu theo quốc gia
Tạo file:

```bash
03_country_city_coverage.png
```

Biểu đồ cho biết:
- Top 15 quốc gia có nhiều thành phố xuất hiện trong dataset nhất

### 5. Tương quan giữa các biến ô nhiễm
Tạo file:

```bash
04_correlation_matrices.png
```

Gồm:
- **Pearson correlation**
- **Spearman correlation**

Các biến được dùng nếu có trong dữ liệu:
- `PM2.5 (ug/m3)`
- `PM10 (ug/m3)`
- `NO (ug/m3)`
- `NO2 (ug/m3)`
- `NH3 (ug/m3)`
- `CO (mg/m3)`
- `SO2 (ug/m3)`
- `O3 (ug/m3)`
- `AQI`
- `Wind_Speed (km/h)`
- `Humidity (%)`

### 6. Phân tích chuỗi thời gian
Tạo các file:

```bash
05_time_series_decomposition.png
06_fft_frequency_analysis.png
```

Nội dung:
- Tính **AQI trung bình theo ngày**
- Phân rã chuỗi thời gian bằng **STL Decomposition**
- Kiểm định tính dừng bằng **ADF Test**
- Phân tích miền tần số bằng **FFT**

### 7. Phân tích riêng cho Việt Nam
Tạo file:

```bash
07_vietnam_top_cities.png
```

Nội dung:
- Lọc dữ liệu có `Country = Vietnam`
- Tính AQI trung bình theo từng thành phố ở Việt Nam
- Vẽ biểu đồ top thành phố Việt Nam có AQI trung bình cao nhất

---

## Danh sách output

Sau khi chạy thành công, thư mục `ph02_eda/outputs/` sẽ có:

| File | Ý nghĩa |
|------|---------|
| `01_descriptive_stats.png` | Thống kê mô tả AQI, PM2.5, top quốc gia |
| `02_top_polluted_cities.png` | Top 10 thành phố ô nhiễm nhất theo mean AQI |
| `03_country_city_coverage.png` | Top 15 quốc gia theo số lượng thành phố |
| `04_correlation_matrices.png` | Ma trận tương quan Pearson và Spearman |
| `05_time_series_decomposition.png` | STL decomposition của AQI trung bình theo ngày |
| `06_fft_frequency_analysis.png` | Phân tích FFT của chuỗi AQI |
| `07_vietnam_top_cities.png` | Top thành phố Việt Nam theo mean AQI |

---

## Giải thích nhanh một số kết quả

| Chỉ số | Ý nghĩa |
|--------|---------|
| Mean AQI cao | Mức độ ô nhiễm trung bình cao hơn |
| Pearson cao | Tương quan tuyến tính mạnh giữa hai biến |
| Spearman cao | Tương quan thứ hạng mạnh, ít nhạy với outlier hơn |
| ADF p-value < 0.05 | Chuỗi thời gian có tính dừng |
| FFT peak rõ | Có thể tồn tại chu kỳ lặp trong dữ liệu |

---

## Lưu ý kỹ thuật

- Script đọc **từng file parquet rồi concat lại**, thay vì `pd.read_parquet()` trực tiếp trên cả thư mục datalake. Cách này giúp tránh lỗi schema mismatch giữa các partition.
- Nếu dataset tăng thêm trong tương lai, thời gian load có thể tăng đáng kể.
- Nếu muốn tối ưu hiệu năng, có thể phân tích theo từng quốc gia trước thay vì đọc toàn bộ thế giới một lần.
- Nếu muốn mở rộng EDA, có thể bổ sung thêm:
  - phân tích theo năm
  - phân tích theo quốc gia
  - top city theo từng giai đoạn
  - heatmap missing values
  - outlier detection

---

## Hướng mở rộng

Có thể phát triển tiếp PH-02 theo các hướng sau:

1. **Country-level EDA**  
   So sánh AQI trung bình giữa các quốc gia.

2. **Yearly trend analysis**  
   Theo dõi xu hướng AQI từ 2014 đến 2025.

3. **Seasonality analysis**  
   So sánh mùa ô nhiễm cao và thấp.

4. **Vietnam deep-dive**  
   Phân tích sâu riêng cho các thành phố ở Việt Nam.

5. **Dashboard / BI integration**  
   Dùng output từ PH-02 làm nguồn cho dashboard trực quan hoá.

---

## Ghi chú

PH-02 hiện đã được điều chỉnh để phù hợp với:
- Dữ liệu Kaggle mới
- Schema AQI mới
- Cấu trúc datalake partition `city/year`
- Quy mô dữ liệu toàn cầu hơn 1.3 triệu records