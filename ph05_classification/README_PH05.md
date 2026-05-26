# PH-05: Classification, Stacking Ensemble & Explainability — An

Module này hoàn thành phần PH-05 theo phân công của An: baseline models, XGBoost/LightGBM/Optuna, Stacking Ensemble, SHAP/LIME/PDP/ICE và MLflow logging/fallback.

## Chạy nhanh để kiểm tra pipeline

```bash
python ph03_preprocessing/scripts/preprocess_features.py
python ph05_classification/scripts/train_classification.py
```

Mặc định script dùng **runtime mode** để chạy nhanh trên laptop:

- `MAX_TRAIN_ROWS=1000`
- `MAX_VAL_ROWS=500`
- `ENABLE_BOOSTING=0`

## Chạy bản đầy đủ hơn cho báo cáo cuối kỳ

```bash
# Linux/Mac
MAX_TRAIN_ROWS=0 MAX_VAL_ROWS=0 ENABLE_BOOSTING=1 python ph05_classification/scripts/train_classification.py

# Windows PowerShell
$env:MAX_TRAIN_ROWS="0"; $env:MAX_VAL_ROWS="0"; $env:ENABLE_BOOSTING="1"; python ph05_classification/scripts/train_classification.py
```

Khi `ENABLE_BOOSTING=1`, script sẽ dùng XGBoost/LightGBM nếu thư viện đã cài. Nếu có `optuna`, script tự tuning; nếu chưa có, script dùng cấu hình mặc định hợp lý.

## Output chính

| File/thư mục | Ý nghĩa |
|---|---|
| `ph05_classification/outputs/baseline_metrics.csv` | Kết quả validation/test của Logistic Regression, Decision Tree, Random Forest, ExtraTrees |
| `final_model_metrics.csv` | Bảng so sánh mô hình cuối trên test set |
| `classification_report_*.csv` | Precision/Recall/F1 theo từng nhãn |
| `confusion_matrix_*_test.png` | Confusion matrix cho từng mô hình |
| `permutation_importance.csv` | Feature importance cho Stacking Ensemble |
| `permutation_importance_top20.png` | Biểu đồ top 20 feature quan trọng |
| `shap_summary_beeswarm_tree_base.png` | SHAP summary cho tree base learner mạnh nhất |
| `pdp_ice_*.png` | PDP/ICE cho các feature quan trọng |
| `models/stacking_ensemble.pkl` | Model Stacking Ensemble đã train |
| `models/label_encoder.pkl` | Label encoder |
| `models/feature_columns.json` | Danh sách feature input theo đúng thứ tự |

## Kiến trúc mô hình

- **Baseline**: Logistic Regression, Decision Tree, Random Forest, ExtraTrees.
- **Boosting optional**: XGBoost và LightGBM, có Optuna tuning nếu cài `optuna`.
- **Stacking Ensemble**: base learners gồm XGBoost/LightGBM khi bật boosting, RandomForest, ExtraTrees; meta learner là Logistic Regression dùng output probability của base learners.
- **Explainability**: permutation importance giải thích Stacking Ensemble; SHAP cho tree base learner; LIME nếu cài `lime`; PDP/ICE cho top features.
- **Logging**: nếu có MLflow thì log run/artifacts; nếu chưa có thì lưu `mlflow_fallback_log.json`.

## Lưu ý kết quả mẫu

Kết quả hiện tại là bản chạy nhanh để chứng minh pipeline. Để lấy số liệu đưa vào báo cáo chính thức, nên chạy full mode và bật boosting.
