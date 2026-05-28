# Tổng hợp phần An — PH-03 & PH-05

## Bối cảnh đề tài mới

Nhóm đã chuyển sang đề tài **AirGlobal: Hệ thống Khai phá Dữ liệu, Phân tích đa chiều và Dự báo Chất lượng Không khí Toàn cầu (2014–2025)**, sử dụng dataset Kaggle World Air Pollution & AQI.

Theo README mới của nhóm, An phụ trách:

- **PH-03:** Tiền xử lý dữ liệu, pipeline, SMOTE-ENN
- **PH-05:** Classification với XGBoost / LightGBM / Optuna

## Phần đã bổ sung

### PH-03

File chính:

```bash
ph03_preprocessing/scripts/preprocess_airglobal.py
```

Chức năng:

- đọc `data/datalake/aqi` hoặc fallback `data/raw/global_air_quality_2014_2025.csv`
- chuẩn hóa schema
- chuẩn hóa target `target_aqi_bucket`
- xử lý duplicate, missing, invalid values, outlier IQR
- tạo feature thời gian, ratios, interactions, frequency encoding, lag/rolling
- chia train/validation/test theo thời gian
- xuất reports và metadata

### PH-05

File chính:

```bash
ph05_classification/scripts/train_airglobal_classification.py
```

Chức năng:

- đọc output PH-03 (`processed_airglobal_features.pkl`, hoặc parquet/csv nếu có)
- loại bỏ cột leakage như `AQI`, `AQI_Bucket`
- train Logistic Regression, Decision Tree, Random Forest, Extra Trees
- train XGBoost / LightGBM nếu có cài
- hỗ trợ Optuna tuning cho LightGBM
- hỗ trợ SMOTE-ENN dạng optional
- train Stacking Ensemble
- đánh giá bằng Accuracy, Macro F1, Weighted F1, Cohen Kappa
- xuất confusion matrix, classification report, feature importance, SHAP nếu chạy được
- lưu production pipeline `.pkl`

## Lệnh chạy

```bash
python ph03_preprocessing/scripts/preprocess_airglobal.py
python ph05_classification/scripts/train_airglobal_classification.py
```

Bản full hơn trên PowerShell:

```powershell
$env:MAX_TRAIN_ROWS="0"
$env:MAX_VAL_ROWS="0"
$env:MAX_TEST_ROWS="0"
$env:ENABLE_BOOSTING="1"
$env:TRAIN_STACKING="1"
python ph05_classification/scripts/train_airglobal_classification.py
```

## Điểm nhấn để thuyết trình

1. Dataset mới có quy mô lớn hơn, nhiều quốc gia/thành phố, phù hợp cho Data Mining và OLAP.
2. PH-03 xử lý dữ liệu theo pipeline rõ ràng và xuất reports minh bạch.
3. PH-05 tránh data leakage bằng cách không dùng trực tiếp `AQI` để dự đoán `AQI_Bucket`.
4. Model được so sánh bằng nhiều metrics, không chỉ Accuracy.
5. Best model được chọn dựa trên validation Macro F1.
6. Có explainability bằng feature importance/SHAP.
