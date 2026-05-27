# Data-Mining-Final
air-pollution-mining-project/
│
├── data/                            # Nơi chứa dữ liệu
│   ├── raw/                         # 103 file CSV tải từ Kaggle (PH-01)
│   └── processed/                   # File sau khi làm sạch & Iceberg Cube (dạng .parquet hoặc .csv)
│
├── notebooks/                       # [PH-02] Chứa các file chạy Google Colab công khai
│   ├── 01_eda_report.ipynb          # Thọ: Phân tích khám phá, xuất file HTML
│   ├── 02_data_warehouse_cube.ipynb # Bảo: Thiết kế mô hình hình sao, tạo Cube bằng Pandas/SQLAlchemy
│   └── 03_machine_learning.ipynb    # An & Huy: Chạy Pipeline, SMOTE-ENN, Optuna, train mô hình & đánh giá
│
├── backend/                         # VÙNG LÀM VIỆC CỦA THỌ (PH-07)
│   ├── app/
│   │   ├── main.py                  # Mã nguồn chính FastAPI
│   │   └── models/                  # Lưu file mô hình tốt nhất (.pkl) sau khi An train xong
│   └── requirements.txt             # Các thư viện cần cài (fastapi, uvicorn, scikit-learn, xgboost)
│
├── frontend/                        # VÙNG LÀM VIỆC CỦA HUY (PH-08)
│   # Nếu làm Web (React) thì chứa source code React, nếu làm Mobile thì chứa source Flutter
│   ├── src/                         
│   ├── package.json
│   └── README.md
│
├── docs/                            # TÀI LIỆU (Cả nhóm)
│   ├── data_dictionary.md           # [PH-01] Thọ viết mô tả ý nghĩa các cột dữ liệu
│   └── user_guide.md                # [PH-08] Huy viết hướng dẫn sử dụng phần mềm
│
└── README.md                        # Giới thiệu tổng quan đồ án và cách chạy nhanh dự án
