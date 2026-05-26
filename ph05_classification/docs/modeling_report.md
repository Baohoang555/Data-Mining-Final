# Báo cáo PH-05 — Classification & Stacking Ensemble

## 1. Mục tiêu

PH-05 xây dựng mô hình phân lớp để dự báo nhãn AQI giờ kế tiếp từ bộ feature đã xử lý ở PH-03. Nhiệm vụ gồm baseline models, boosting models, stacking ensemble và giải thích mô hình bằng SHAP/LIME/PDP/ICE.

## 2. Dataset đầu vào

- Input: `ph03_preprocessing/outputs/processed_aqi_features.csv`.
- Target: `target_aqi_label_next_1h`.
- Số feature: 155.
- Split dùng từ PH-03: train/validation/test, trong đó test là timestamp cuối cùng để tránh leakage thời gian.

## 3. Mô hình

Các baseline đã triển khai:

- Logistic Regression với `class_weight='balanced'`.
- Decision Tree với `class_weight='balanced'`.
- Random Forest với `class_weight='balanced'`.
- ExtraTrees với `class_weight='balanced'`.

Các mô hình boosting đã có code:

- XGBoost với search space Optuna: `max_depth`, `learning_rate`, `n_estimators`, `subsample`, `colsample_bytree`, `min_child_weight`.
- LightGBM với search space Optuna: `num_leaves`, `min_child_samples`, `max_depth`, `learning_rate`, `n_estimators`, `subsample`, `colsample_bytree`.

Stacking Ensemble:

- Base learners: XGBoost/LightGBM khi bật `ENABLE_BOOSTING=1`, RandomForest và ExtraTrees.
- Meta learner: Logistic Regression.
- Input của meta learner là xác suất dự đoán từ base learners (`predict_proba`).

## 4. Kết quả chạy nhanh hiện tại

Script đã chạy ở runtime mode để kiểm tra end-to-end pipeline. Kết quả mẫu trên test set:

| Model | Accuracy | Weighted F1 | Macro F1 | Cohen's Kappa |
|---|---:|---:|---:|---:|
| DecisionTree | 0.6678 | 0.6711 | 0.6602 | 0.5170 |
| RandomForest | 0.6524 | 0.6422 | 0.5709 | 0.4754 |
| ExtraTrees | 0.6437 | 0.6303 | 0.6107 | 0.4665 |
| LogisticRegression | 0.5598 | 0.5653 | 0.5426 | 0.3665 |
| StackingEnsemble | 0.4989 | 0.5127 | 0.4394 | 0.3374 |

Lưu ý: đây là kết quả chạy nhanh với `MAX_TRAIN_ROWS=1000`, `MAX_VAL_ROWS=500`, `ENABLE_BOOSTING=0`. Để lấy kết quả chính thức, cần chạy full mode:

```bash
MAX_TRAIN_ROWS=0 MAX_VAL_ROWS=0 ENABLE_BOOSTING=1 python ph05_classification/scripts/train_classification.py
```

## 5. Explainability

Artifacts đã tạo:

- `permutation_importance.csv`: top feature ảnh hưởng đến weighted F1 của Stacking Ensemble.
- `permutation_importance_top20.png`: biểu đồ top 20 feature quan trọng nhất.
- `shap_summary_beeswarm_tree_base.png`: SHAP summary cho tree base learner.
- `pdp_ice_*.png`: PDP/ICE cho các feature top đầu.
- `classification_report_*.csv`: precision/recall/F1 theo từng lớp.
- `confusion_matrix_*_test.png`: confusion matrix để phân tích nhãn hay nhầm.

## 6. Nhận xét

Do dữ liệu weather chưa overlap với AQI, mô hình chủ yếu học từ pollutant, lag/rolling và time/spatial features. Lớp `Hazardous` rất ít nên macro F1 thấp hơn weighted F1. Khi chạy full mode, nên bật XGBoost/LightGBM và cân nhắc SMOTEENN trên train set để cải thiện lớp hiếm.
