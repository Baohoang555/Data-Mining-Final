# Data-Mining-Final
# AirGlobal: Hệ thống Khai phá Dữ liệu, Phân tích đa chiều và Dự báo Chất lượng Không khí Toàn cầu (2014 - 2025)

## 📌 Tổng quan dự án
Dự án tập trung vào việc xây dựng một hệ thống khai phá dữ liệu End-to-End quy mô lớn nhằm quản lý, phân tích đa chiều (OLAP) và dự báo chỉ số chất lượng không khí (AQI) trên toàn thế giới dựa trên bộ dữ liệu thực tế gồm **103 tập tin** (~1.35 triệu dòng dữ liệu). Hệ thống tích hợp các mô hình học máy hiện đại để đưa ra cảnh báo sớm về ô nhiễm, phục vụ cho việc hỗ trợ ra quyết định (DSS).

* **Bộ dữ liệu gốc:** [World Air Pollution & AQI Dataset (2014-2025) - Kaggle](https://www.kaggle.com/datasets/ashyou09/world-air-pollution-and-aqi-dataset-20142025)
* **Quy mô dữ liệu:** 1.349.280 dòng.

---

## 👥 Thành viên nhóm & Phân công công việc

| Thành viên | Vai trò chính | Các pha phụ trách (Phases) |
| :--- | :--- | :--- |
| **Thọ** | Data Engineer & Backend | **PH-01:** Thu thập dữ liệu <br>**PH-02:** Phân tích khám phá (EDA) <br>**PH-07:** Triển khai Backend & API |
| **An** | Data Scientist | **PH-03:** Tiền xử lý (Pipeline + SMOTE-ENN) <br>**PH-05:** Xây dựng mô hình Classification (XGBoost/LightGBM/Optuna) |
| **Bảo** | Data Warehouse Engineer | **PH-04:** Thiết kế Data Warehouse & Tạo lập Iceberg Cube |
| **Huy** | Frontend Developer & QA | **PH-06:** Đánh giá & Kiểm thử mô hình (Robustness test) <br>**PH-08:** Triển khai Giao diện người dùng (Web/Mobile) |

---

## 📂 Cấu trúc thư mục dự án

```text
air-pollution-mining-project/
│
├── data/                            # Nơi quản lý dữ liệu dự án
│   ├── raw/                         # Chứa 103 file CSV gốc tải từ Kaggle (PH-01)
│   └── processed/                   # Dữ liệu sạch & Khối lập phương Iceberg Cube (.parquet / .csv)
│
├── notebooks/                       # Môi trường thực nghiệm trên Google Colab
│   ├── 01_eda_report.ipynb          # [Thọ] Phân tích khám phá, trực quan không gian & xuất báo cáo HTML
│   ├── 02_data_warehouse_cube.ipynb # [Bảo] Thiết kế Star Schema, tạo lập Cube + Điều kiện Iceberg
│   └── 03_machine_learning.ipynb    # [An & Huy] Pipeline xử lý, cân bằng dữ liệu, tối ưu Optuna & Đánh giá
│
├── backend/                         # [Thọ] Mã nguồn dịch vụ Backend phục vụ Real-time Inference
│   ├── app/
│   │   ├── main.py                  # Điểm khởi chạy FastAPI chính
│   │   └── models/                  # Lưu trữ file mô hình tối ưu nhất sau khi huấn luyện (.pkl)
│   └── requirements.txt             # Danh sách thư viện Backend (FastAPI, Uvicorn, Scikit-learn, XGBoost...)
│
├── frontend/                        # [Huy] Giao diện người dùng hiển thị Analytics Dashboard & Prediction Portal
│   ├── src/                         # Mã nguồn ứng dụng
│   └── package.json                 # Cấu hình dự án Frontend
│
├── docs/                            # Tài liệu kỹ thuật của dự án
│   ├── data_dictionary.md           # [Thọ] Từ điển dữ liệu, định nghĩa các thuộc tính và chỉ số đo đạc
│   └── user_guide.md                # [Huy] Hướng dẫn sử dụng hệ thống chi tiết cho người dùng
│
└── README.md                        # Tài liệu hướng dẫn tổng quan dự án (File này)
