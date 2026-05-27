# Data Dictionary

Tài liệu mô tả dữ liệu sử dụng trong project sau khi chuyển sang nguồn Kaggle:

**Dataset:** World Air Pollution & AQI Dataset (2014–2025)  
**Nguồn:** Kaggle  
**Pipeline sử dụng:** Download trong `raw.ipynb` → lưu `data/raw` → build Parquet datalake tại `data/datalake/aqi`

---

## 1. Raw Dataset

Dữ liệu gốc được lưu trong:

```bash
data/raw/
```

Dataset gồm:
- File tổng hợp lớn: `global_air_quality_2014_2025.csv`
- Nhiều thư mục / file CSV con theo quốc gia
- Tất cả các file CSV được đọc và concat để tạo full dataset toàn cầu

Tổng quy mô sau khi tổng hợp:
- **1,349,280 records**
- **2,271 cities**
- Giai đoạn: **2014–2025**

---

## 2. AQI Datalake

Dữ liệu sau khi chuẩn hoá được lưu tại:

```bash
data/datalake/aqi/
```

Cấu trúc partition:

```bash
data/datalake/aqi/{city}/{year}/data.parquet
```

Ví dụ:

```bash
data/datalake/aqi/10th_of_ramadan/2014/data.parquet
data/datalake/aqi/ho_chi_minh_city/2020/data.parquet
```

---

## 3. Schema chính của dataset

| Thuộc tính | Kiểu dữ liệu | Mô tả | Nguồn |
|-----------|-------------|------|------|
| Country | string | Tên quốc gia | Kaggle dataset |
| State | string | Bang / tiểu bang / vùng hành chính cấp 1 (nếu có) | Kaggle dataset |
| City | string | Tên thành phố | Kaggle dataset |
| Date | datetime | Ngày quan sát / ghi nhận dữ liệu | Kaggle dataset, chuẩn hoá trong pipeline |
| PM2.5 (ug/m3) | float | Nồng độ bụi mịn PM2.5 | Kaggle dataset |
| PM10 (ug/m3) | float | Nồng độ bụi PM10 | Kaggle dataset |
| NO (ug/m3) | float | Nồng độ Nitric Oxide | Kaggle dataset |
| NO2 (ug/m3) | float | Nồng độ Nitrogen Dioxide | Kaggle dataset |
| NOx (ppb) | float | Nồng độ Nitrogen Oxides | Kaggle dataset |
| NH3 (ug/m3) | float | Nồng độ Amoniac | Kaggle dataset |
| CO (mg/m3) | float | Nồng độ Carbon Monoxide | Kaggle dataset |
| SO2 (ug/m3) | float | Nồng độ Sulfur Dioxide | Kaggle dataset |
| O3 (ug/m3) | float | Nồng độ Ozone | Kaggle dataset |
| Benzene (ug/m3) | float | Nồng độ Benzen | Kaggle dataset |
| Toluene (ug/m3) | float | Nồng độ Toluen | Kaggle dataset |
| Xylene (ug/m3) | float | Nồng độ Xylen | Kaggle dataset |
| AQI | float | Chỉ số chất lượng không khí tổng hợp | Kaggle dataset |
| AQI_Bucket | string | Nhóm / mức phân loại AQI | Kaggle dataset |
| Wind_Speed (km/h) | float | Tốc độ gió | Kaggle dataset |
| Humidity (%) | float | Độ ẩm không khí | Kaggle dataset |
| Deforestation_Rate_% | float | Tỷ lệ mất rừng | Kaggle dataset |
| Industry_Growth_% | float | Tốc độ tăng trưởng công nghiệp | Kaggle dataset |
| CO2_Emission_MT | float | Lượng phát thải CO2 | Kaggle dataset |
| Population_Density_per_SqKm | float | Mật độ dân số theo km² | Kaggle dataset |
| Division | string | Đơn vị hành chính dạng division (nếu có) | Kaggle dataset |
| Province | string | Tỉnh / tỉnh thành (nếu có) | Kaggle dataset |
| Region | string | Vùng / khu vực (nếu có) | Kaggle dataset |
| Prefecture | string | Prefecture (đối với một số quốc gia) | Kaggle dataset |
| Federal_District | string | Khu vực liên bang (nếu có) | Kaggle dataset |
| year | int | Năm tách ra từ cột `Date`, dùng để partition datalake | Computed |

---

## 4. Ý nghĩa các nhóm biến

### 4.1. Nhóm định danh địa lý
Các cột:
- `Country`
- `State`
- `City`
- `Division`
- `Province`
- `Region`
- `Prefecture`
- `Federal_District`

Nhóm này dùng để xác định vị trí địa lý và hỗ trợ phân tích theo quốc gia, vùng, thành phố.

### 4.2. Nhóm chỉ số ô nhiễm không khí
Các cột:
- `PM2.5 (ug/m3)`
- `PM10 (ug/m3)`
- `NO (ug/m3)`
- `NO2 (ug/m3)`
- `NOx (ppb)`
- `NH3 (ug/m3)`
- `CO (mg/m3)`
- `SO2 (ug/m3)`
- `O3 (ug/m3)`
- `Benzene (ug/m3)`
- `Toluene (ug/m3)`
- `Xylene (ug/m3)`
- `AQI`
- `AQI_Bucket`

Đây là nhóm biến cốt lõi cho bài toán phân tích chất lượng không khí.

### 4.3. Nhóm điều kiện môi trường - xã hội
Các cột:
- `Wind_Speed (km/h)`
- `Humidity (%)`
- `Deforestation_Rate_%`
- `Industry_Growth_%`
- `CO2_Emission_MT`
- `Population_Density_per_SqKm`

Nhóm này hỗ trợ phân tích mối liên hệ giữa ô nhiễm không khí và các yếu tố môi trường / phát triển.

### 4.4. Nhóm thời gian
Các cột:
- `Date`
- `year`

Nhóm này phục vụ phân tích chuỗi thời gian, trend, seasonality, và partition dữ liệu trong datalake.

---

## 5. Cột được tạo thêm trong pipeline

Các cột dưới đây không phải cột gốc hoàn toàn từ raw CSV, mà được tạo hoặc chuẩn hoá trong quá trình xử lý:

| Thuộc tính | Kiểu dữ liệu | Mô tả |
|-----------|-------------|------|
| year | int | Trích xuất từ `Date` để phục vụ partition datalake |
| city_partition | string | Cột tạm dùng để chuẩn hoá tên thư mục partition (không lưu trong file parquet cuối) |

---

## 6. Quy ước làm sạch dữ liệu

Trong pipeline `raw.ipynb`, dữ liệu được xử lý theo các bước:

1. Download toàn bộ dataset từ Kaggle vào `data/raw`
2. Quét tất cả file `.csv` trong thư mục raw
3. Đọc và concat thành một DataFrame thống nhất
4. Parse cột `Date` sang kiểu datetime
5. Tạo cột `year`
6. Chuẩn hoá `City` thành `city_partition`
7. Ghi Parquet theo cấu trúc `city/year`

---

## 7. Ghi chú sử dụng

- Cột `city_partition` chỉ dùng trong bước build datalake, **không phải biến phân tích chính**.
- Một số cột địa lý như `State`, `Division`, `Province`, `Region`, `Prefecture`, `Federal_District` có thể bị thiếu ở nhiều quốc gia.
- Không phải tất cả records đều có đầy đủ toàn bộ biến ô nhiễm.
- Khi phân tích, nên kiểm tra missing values trước khi tính correlation hoặc modelling.
- Dữ liệu hiện tại được dùng trực tiếp cho PH-02 (EDA) từ `data/datalake/aqi`.

---

## 8. Tổng quan số lượng biến

| Nhóm | Số lượng |
|------|----------|
| Địa lý | 8 |
| Ô nhiễm không khí | 14 |
| Môi trường - xã hội | 6 |
| Thời gian | 2 |
| Biến tạo thêm | 2 |

Tổng số cột phân tích chính: **30 cột**  
(Tính cả `year`, không tính `city_partition` vì đây là cột tạm)

---

## 9. Tóm tắt

Data dictionary này áp dụng cho phiên bản project đã chuyển từ:
- **API crawling** → sang **Kaggle dataset**
- **JSON raw** → sang **CSV raw**
- **station-based schema** → sang **global city-based schema**
- **legacy build_datalake.py** → sang **pipeline tích hợp trong `raw.ipynb`**