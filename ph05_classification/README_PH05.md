# PH-05: Classification Modeling — An

Module này xử lý phần **PH-05** cho đề tài AirGlobal.

## Mục tiêu

Dự đoán `target_aqi_bucket` từ các feature ô nhiễm, môi trường, thời gian và địa lý đã được xử lý ở PH-03.

Target sau chuẩn hóa gồm 6 nhóm:

| Label | Ý nghĩa |
|---|---|
| `Good` | Tốt |
| `Satisfactory` | Khá / chấp nhận được |
| `Moderate` | Trung bình |
| `Unhealthy` | Kém / không lành mạnh |
| `Very_Unhealthy` | Rất xấu |
| `Hazardous` | Nguy hại |

## Model được triển khai

Script `train_airglobal_classification.py` train và so sánh:

- Logistic Regression
- Decision Tree
- Random Forest
- Extra Trees
- XGBoost nếu đã cài
- LightGBM nếu đã cài
- Stacking Ensemble nếu có đủ base models
- LightGBM + Optuna nếu bật `OPTUNA_TRIALS > 0`

## Cách chạy cơ bản

Trước hết chạy PH-03:

```bash
python ph03_preprocessing/scripts/preprocess_airglobal.py
```

Sau đó chạy PH-05:

```bash
python ph05_classification/scripts/train_airglobal_classification.py
```

## Chạy bản full hơn

PowerShell:

```powershell
$env:MAX_TRAIN_ROWS="0"
$env:MAX_VAL_ROWS="0"
$env:MAX_TEST_ROWS="0"
$env:ENABLE_BOOSTING="1"
$env:TRAIN_STACKING="1"
python ph05_classification/scripts/train_airglobal_classification.py
```

CMD:

```cmd
set MAX_TRAIN_ROWS=0
set MAX_VAL_ROWS=0
set MAX_TEST_ROWS=0
set ENABLE_BOOSTING=1
set TRAIN_STACKING=1
python ph05_classification/scripts/train_airglobal_classification.py
```

## Optional packages

Nên cài thêm để có kết quả đẹp hơn:

```bash
pip install xgboost lightgbm optuna shap imbalanced-learn
```

## Biến môi trường hữu ích

| Biến | Mặc định | Ý nghĩa |
|---|---:|---|
| `MAX_TRAIN_ROWS` | `150000` | Giới hạn train rows cho máy yếu; `0` = full |
| `MAX_VAL_ROWS` | `50000` | Giới hạn validation rows; `0` = full |
| `MAX_TEST_ROWS` | `50000` | Giới hạn test rows; `0` = full |
| `ENABLE_BOOSTING` | `1` | Bật XGBoost/LightGBM nếu có cài |
| `TRAIN_STACKING` | `1` | Bật Stacking Ensemble |
| `STACKING_MAX_ROWS` | `80000` | Giới hạn số dòng dùng train stacking |
| `USE_SMOTEENN` | `0` | Bật SMOTE-ENN. Nên bật khi chạy sample vì full data rất nặng |
| `SMOTEENN_MAX_ROWS` | `60000` | Nếu train rows lớn hơn mức này thì tự skip SMOTE-ENN |
| `OPTUNA_TRIALS` | `0` | Số trials Optuna cho LightGBM; ví dụ `30`, `50`, `100` |
| `RUN_SHAP` | `1` | Cố gắng xuất SHAP summary nếu model hỗ trợ |
| `SHAP_SAMPLE_ROWS` | `1000` | Số dòng test dùng cho SHAP |

## Output

Sau khi chạy, thư mục `ph05_classification/outputs/` có:

| File | Ý nghĩa |
|---|---|
| `model_metrics.csv` | So sánh Accuracy, Macro F1, Weighted F1, Kappa |
| `classification_report_best_model.txt` | Report chi tiết best model |
| `classification_report_best_model.csv` | Report dạng bảng |
| `confusion_matrix_best_model.png` | Ma trận nhầm lẫn |
| `best_model_feature_importance.csv` | Feature importance |
| `best_model_feature_importance_top20.png` | Top 20 feature quan trọng |
| `best_model_shap_summary.png` | SHAP summary nếu chạy được |
| `model_run_metadata.json` | Metadata run model |
| `label_mapping.json` | Mapping label index → label name |

Model lưu ở `ph05_classification/models/`:

| File | Ý nghĩa |
|---|---|
| `best_aqi_classifier_pipeline.pkl` | Pipeline production gồm preprocessing + best model |
| `label_encoder.pkl` | Encoder nhãn target |
| `stacking_ensemble_transformed.pkl` | Model stacking trên feature matrix đã transform |

## Lưu ý khi báo cáo

Không nên nói trước rằng Stacking chắc chắn tốt nhất. Nên trình bày theo hướng thực nghiệm:

> Nhóm em triển khai nhiều mô hình baseline và ensemble, sau đó chọn mô hình tốt nhất dựa trên Macro F1 ở validation set. Stacking Ensemble được triển khai theo yêu cầu đề tài, tuy nhiên mô hình cuối cùng sẽ được chọn dựa trên kết quả thực nghiệm thay vì giả định trước.
