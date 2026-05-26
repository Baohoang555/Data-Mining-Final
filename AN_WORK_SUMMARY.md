# Phần việc của An đã bổ sung

## PH-03 — Tiền xử lý dữ liệu

Đã thêm module `ph03_preprocessing/` gồm script xử lý dữ liệu, output reports và báo cáo markdown.

Nội dung hoàn thành:

- Missing value analysis: MCAR/MAR/MNAR-like.
- Linear interpolation cho gap nhỏ dưới 3 giờ.
- KNN/grouped imputation cho gap dài.
- IQR outlier theo trạm/tháng.
- Phân biệt sensor error và sự kiện ô nhiễm thật.
- Lag features 1h, 3h, 6h, 12h, 24h.
- Rolling features 3h, 6h, 24h.
- Cyclical time features và spatial features.
- Target `target_aqi_label_next_1h`.
- Split train/validation/test tránh data leakage.

## PH-05 — Classification

Đã thêm module `ph05_classification/` gồm script train model, artifacts kết quả mẫu và báo cáo markdown.

Nội dung hoàn thành:

- Baseline models: Logistic Regression, Decision Tree, Random Forest, ExtraTrees.
- Code XGBoost/LightGBM + Optuna tuning khi bật full mode.
- Stacking Ensemble với Logistic Regression meta learner.
- Confusion matrix, classification report, weighted F1, macro F1, accuracy, Cohen's Kappa.
- Permutation importance, SHAP, PDP/ICE, LIME optional.
- MLflow logging nếu có thư viện, fallback JSON nếu chưa cài.

## Lệnh chạy

```bash
python ph03_preprocessing/scripts/preprocess_features.py
python ph05_classification/scripts/train_classification.py
```

Chạy bản đầy đủ:

```bash
MAX_TRAIN_ROWS=0 MAX_VAL_ROWS=0 ENABLE_BOOSTING=1 python ph05_classification/scripts/train_classification.py
```

## Ghi chú chất lượng dữ liệu

Dữ liệu weather trong zip không overlap timestamp với AQI, nên weather features hiện bị impute fallback. Nên yêu cầu Thọ crawl lại weather cùng giai đoạn AQI để mô hình phản ánh đúng ảnh hưởng thời tiết.
