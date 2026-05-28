# An Add-on: PH-03 + PH-05 cho AirGlobal Dataset

Gói này chứa phần hoàn thiện của An cho repo Data-Mining-Final sau khi nhóm đổi sang dataset AirGlobal/Kaggle.

## Cách dùng

Copy các thư mục/file trong gói này vào thư mục gốc repo của nhóm:

```text
ph03_preprocessing/
ph05_classification/
AN_WORK_SUMMARY.md
requirements_an.txt
```

Sau đó chạy:

```bash
pip install -r requirements_an.txt
python ph03_preprocessing/scripts/preprocess_airglobal.py
python ph05_classification/scripts/train_airglobal_classification.py
```

## Lưu ý

- Gói này **không kèm full processed dataset** `processed_airglobal_features.pkl` vì file này có thể lớn. Chạy PH-03 sẽ tự sinh lại.
- Trong `ph03_preprocessing/outputs/` có sample 5000 dòng và các report mẫu để xem nhanh.
- Trong `ph05_classification/outputs/` có output mẫu từ lần chạy nhanh để kiểm tra format. Kết quả chính thức nên chạy lại trên máy của nhóm.
- Nếu muốn xuất full CSV từ PH-03, chạy:

```bash
SAVE_FULL_CSV=1 python ph03_preprocessing/scripts/preprocess_airglobal.py
```

PowerShell:

```powershell
$env:SAVE_FULL_CSV="1"
python ph03_preprocessing/scripts/preprocess_airglobal.py
```
