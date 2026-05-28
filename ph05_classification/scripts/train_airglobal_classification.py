"""
PH-05: Classification Modeling — AirGlobal AQI Dataset
Author: An

Mục tiêu:
- Dùng dữ liệu đã xử lý từ PH-03 để dự đoán target_aqi_bucket.
- Tránh data leakage: không dùng AQI numeric hoặc AQI_Bucket gốc làm feature.
- So sánh baseline + tree ensemble + boosting + stacking.
- Hỗ trợ class imbalance bằng class_weight và tùy chọn SMOTE-ENN.
- Xuất metrics, confusion matrix, feature importance, SHAP fallback và model .pkl.

Chạy nhanh từ thư mục gốc project:
    python ph05_classification/scripts/train_airglobal_classification.py

Chạy full hơn nếu máy đủ mạnh:
    # PowerShell
    $env:MAX_TRAIN_ROWS="0"; $env:MAX_VAL_ROWS="0"; $env:MAX_TEST_ROWS="0"; $env:TRAIN_STACKING="1"
    python ph05_classification/scripts/train_airglobal_classification.py
"""

from __future__ import annotations

import json
import os
import warnings
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, StackingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    cohen_kappa_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils.class_weight import compute_sample_weight

warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).resolve().parents[2]
PH03_OUTPUT_DIR = BASE_DIR / "ph03_preprocessing" / "outputs"
INPUT_PKL = PH03_OUTPUT_DIR / "processed_airglobal_features.pkl"
INPUT_PARQUET = PH03_OUTPUT_DIR / "processed_airglobal_features.parquet"
INPUT_CSV = PH03_OUTPUT_DIR / "processed_airglobal_features.csv"
FEATURE_CATALOG = PH03_OUTPUT_DIR / "feature_catalog.csv"
OUTPUT_DIR = BASE_DIR / "ph05_classification" / "outputs"
MODEL_DIR = BASE_DIR / "ph05_classification" / "models"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

TARGET_COL = "target_aqi_bucket"
SPLIT_COL = "split"
DATE_COL = "date"
LEAKAGE_COLUMNS = {"aqi", "aqi_bucket", "aqi_bucket_clean", TARGET_COL, SPLIT_COL, DATE_COL}
RANDOM_STATE = 42

DEFAULT_MAX_TRAIN_ROWS = int(os.getenv("MAX_TRAIN_ROWS", "50000"))
DEFAULT_MAX_VAL_ROWS = int(os.getenv("MAX_VAL_ROWS", "10000"))
DEFAULT_MAX_TEST_ROWS = int(os.getenv("MAX_TEST_ROWS", "10000"))
ENABLE_BOOSTING = os.getenv("ENABLE_BOOSTING", "1") == "1"
TRAIN_STACKING = os.getenv("TRAIN_STACKING", "0") == "1"
STACKING_MAX_ROWS = int(os.getenv("STACKING_MAX_ROWS", "30000"))
USE_SMOTEENN = os.getenv("USE_SMOTEENN", "0") == "1"
SMOTEENN_MAX_ROWS = int(os.getenv("SMOTEENN_MAX_ROWS", "60000"))
OPTUNA_TRIALS = int(os.getenv("OPTUNA_TRIALS", "0"))
RUN_SHAP = os.getenv("RUN_SHAP", "1") == "1"
SHAP_SAMPLE_ROWS = int(os.getenv("SHAP_SAMPLE_ROWS", "1000"))

LABEL_VI = {
    "Good": "Tốt",
    "Satisfactory": "Khá / Chấp nhận được",
    "Moderate": "Trung bình",
    "Unhealthy": "Kém / Không lành mạnh",
    "Very_Unhealthy": "Rất xấu",
    "Hazardous": "Nguy hại",
}


@dataclass
class ModelRunSummary:
    rows_train: int
    rows_val: int
    rows_test: int
    feature_count: int
    categorical_feature_count: int
    numeric_feature_count: int
    best_model_by_val_macro_f1: str
    best_val_macro_f1: float
    best_test_macro_f1: float
    best_test_weighted_f1: float
    best_test_accuracy: float
    smoteenn_used: bool
    optuna_trials: int
    notes: List[str]


def log(msg: str) -> None:
    print(msg, flush=True)


def env_sample(df: pd.DataFrame, max_rows: int, label_col: str) -> pd.DataFrame:
    """Stratified downsample for laptop-friendly experiments. max_rows=0 means full data."""
    if max_rows <= 0 or len(df) <= max_rows:
        return df
    if df[label_col].nunique() < 2:
        return df.sample(n=max_rows, random_state=RANDOM_STATE)
    splitter = StratifiedShuffleSplit(n_splits=1, train_size=max_rows, random_state=RANDOM_STATE)
    idx, _ = next(splitter.split(df, df[label_col]))
    return df.iloc[idx].copy()


def load_processed_data() -> Tuple[pd.DataFrame, List[str], List[str]]:
    if INPUT_PKL.exists():
        df = pd.read_pickle(INPUT_PKL)
    elif INPUT_PARQUET.exists():
        df = pd.read_parquet(INPUT_PARQUET)
    elif INPUT_CSV.exists():
        df = pd.read_csv(INPUT_CSV)
    else:
        raise FileNotFoundError(
            f"Không tìm thấy processed dataset trong {PH03_OUTPUT_DIR}. Hãy chạy: python ph03_preprocessing/scripts/preprocess_airglobal.py"
        )

    if TARGET_COL not in df.columns:
        raise ValueError(f"Processed dataset thiếu target column: {TARGET_COL}")
    if SPLIT_COL not in df.columns:
        raise ValueError(f"Processed dataset thiếu split column: {SPLIT_COL}")

    if FEATURE_CATALOG.exists():
        catalog = pd.read_csv(FEATURE_CATALOG)
        feature_cols = [c for c in catalog["feature"].tolist() if c in df.columns and c not in LEAKAGE_COLUMNS]
        categorical_features = [
            c for c in catalog.loc[catalog["feature_type"] == "categorical", "feature"].tolist()
            if c in feature_cols
        ]
        numeric_features = [c for c in feature_cols if c not in categorical_features]
    else:
        feature_cols = [c for c in df.columns if c not in LEAKAGE_COLUMNS]
        categorical_features = [c for c in feature_cols if str(df[c].dtype) in ["object", "string", "category"]]
        numeric_features = [c for c in feature_cols if c not in categorical_features]

    # Ensure object columns that slipped through are treated as categorical.
    for col in feature_cols:
        if str(df[col].dtype) in ["object", "string", "category"] and col not in categorical_features:
            categorical_features.append(col)
            if col in numeric_features:
                numeric_features.remove(col)

    return df, numeric_features, categorical_features


def make_one_hot_encoder() -> OneHotEncoder:
    # sklearn 1.2+ uses sparse_output; sklearn 1.1 uses sparse.
    try:
        return OneHotEncoder(handle_unknown="ignore", min_frequency=50, sparse_output=True)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=True)


def build_preprocessor(numeric_features: List[str], categorical_features: List[str]) -> ColumnTransformer:
    numeric_pipe = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler(with_mean=False)),
    ])
    categorical_pipe = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", make_one_hot_encoder()),
    ])

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, numeric_features),
            ("cat", categorical_pipe, categorical_features),
        ],
        remainder="drop",
        sparse_threshold=0.3,
    )


def get_feature_names(preprocessor: ColumnTransformer, numeric_features: List[str], categorical_features: List[str]) -> List[str]:
    try:
        return list(preprocessor.get_feature_names_out())
    except Exception:
        names = [f"num__{c}" for c in numeric_features]
        try:
            ohe = preprocessor.named_transformers_["cat"].named_steps["onehot"]
            cat_names = list(ohe.get_feature_names_out(categorical_features))
            names += [f"cat__{c}" for c in cat_names]
        except Exception:
            names += [f"cat__{c}" for c in categorical_features]
        return names


def maybe_apply_smoteenn(X_train, y_train):
    notes = []
    if not USE_SMOTEENN:
        return X_train, y_train, False, notes
    if len(y_train) > SMOTEENN_MAX_ROWS:
        notes.append(f"SMOTE-ENN skipped because train rows {len(y_train):,} > SMOTEENN_MAX_ROWS={SMOTEENN_MAX_ROWS:,}.")
        return X_train, y_train, False, notes
    try:
        from imblearn.combine import SMOTEENN
        sampler = SMOTEENN(random_state=RANDOM_STATE)
        X_res, y_res = sampler.fit_resample(X_train, y_train)
        notes.append(f"SMOTE-ENN applied: {len(y_train):,} -> {len(y_res):,} rows.")
        return X_res, y_res, True, notes
    except Exception as exc:
        notes.append(f"SMOTE-ENN skipped due to {type(exc).__name__}: {exc}")
        return X_train, y_train, False, notes


def get_optional_models(num_classes: int) -> Dict[str, object]:
    models: Dict[str, object] = {}
    if not ENABLE_BOOSTING:
        return models

    try:
        from xgboost import XGBClassifier
        models["XGBoost"] = XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            objective="multi:softprob",
            eval_metric="mlogloss",
            tree_method="hist",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )
    except Exception as exc:
        log(f"  ⚠️  XGBoost unavailable: {type(exc).__name__}")

    try:
        from lightgbm import LGBMClassifier
        models["LightGBM"] = LGBMClassifier(
            n_estimators=250,
            learning_rate=0.05,
            num_leaves=63,
            max_depth=-1,
            subsample=0.9,
            colsample_bytree=0.9,
            class_weight="balanced",
            random_state=RANDOM_STATE,
            n_jobs=-1,
            verbose=-1,
        )
    except Exception as exc:
        log(f"  ⚠️  LightGBM unavailable: {type(exc).__name__}")

    return models


def tune_lightgbm_with_optuna(X_train, y_train, X_val, y_val, num_classes: int):
    if OPTUNA_TRIALS <= 0:
        return None, "Optuna disabled. Set OPTUNA_TRIALS > 0 to tune."
    try:
        import optuna
        from lightgbm import LGBMClassifier
    except Exception as exc:
        return None, f"Optuna/LightGBM unavailable: {type(exc).__name__}: {exc}"

    def objective(trial):
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 150, 700),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.2, log=True),
            "num_leaves": trial.suggest_int("num_leaves", 15, 127),
            "max_depth": trial.suggest_int("max_depth", 3, 12),
            "min_child_samples": trial.suggest_int("min_child_samples", 10, 120),
            "subsample": trial.suggest_float("subsample", 0.65, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.65, 1.0),
            "reg_alpha": trial.suggest_float("reg_alpha", 1e-8, 5.0, log=True),
            "reg_lambda": trial.suggest_float("reg_lambda", 1e-8, 5.0, log=True),
            "class_weight": "balanced",
            "random_state": RANDOM_STATE,
            "n_jobs": -1,
            "verbose": -1,
        }
        model = LGBMClassifier(**params)
        model.fit(X_train, y_train)
        pred = model.predict(X_val)
        return f1_score(y_val, pred, average="macro", zero_division=0)

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=OPTUNA_TRIALS, show_progress_bar=False)

    best_params = study.best_params
    best_params.update({"class_weight": "balanced", "random_state": RANDOM_STATE, "n_jobs": -1, "verbose": -1})
    tuned = LGBMClassifier(**best_params)
    tuned.fit(X_train, y_train)
    with open(OUTPUT_DIR / "optuna_lightgbm_best_params.json", "w", encoding="utf-8") as f:
        json.dump({"best_value_macro_f1": study.best_value, "best_params": study.best_params}, f, indent=2)
    return tuned, f"Optuna LightGBM tuned with {OPTUNA_TRIALS} trials. Best val macro F1={study.best_value:.4f}"


def evaluate_model(name: str, model, X, y, split: str) -> Dict[str, object]:
    pred = model.predict(X)
    return {
        "model": name,
        "split": split,
        "accuracy": accuracy_score(y, pred),
        "macro_f1": f1_score(y, pred, average="macro", zero_division=0),
        "weighted_f1": f1_score(y, pred, average="weighted", zero_division=0),
        "macro_precision": precision_score(y, pred, average="macro", zero_division=0),
        "macro_recall": recall_score(y, pred, average="macro", zero_division=0),
        "cohen_kappa": cohen_kappa_score(y, pred),
    }


def plot_confusion_matrix(y_true, y_pred, labels: List[str], output_path: Path, title: str) -> None:
    cm = confusion_matrix(y_true, y_pred, labels=list(range(len(labels))))
    fig, ax = plt.subplots(figsize=(9, 7))
    im = ax.imshow(cm, interpolation="nearest")
    ax.figure.colorbar(im, ax=ax)
    ax.set(
        xticks=np.arange(len(labels)),
        yticks=np.arange(len(labels)),
        xticklabels=labels,
        yticklabels=labels,
        ylabel="True label",
        xlabel="Predicted label",
        title=title,
    )
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    thresh = cm.max() / 2 if cm.max() else 0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], "d"), ha="center", va="center")
    fig.tight_layout()
    plt.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def save_feature_importance(model, feature_names: List[str], output_prefix: str) -> Optional[pd.DataFrame]:
    importance = None
    if hasattr(model, "feature_importances_"):
        importance = np.asarray(model.feature_importances_, dtype=float)
    elif hasattr(model, "coef_"):
        coef = np.asarray(model.coef_, dtype=float)
        importance = np.mean(np.abs(coef), axis=0) if coef.ndim == 2 else np.abs(coef)

    if importance is None:
        return None

    n = min(len(feature_names), len(importance))
    imp_df = pd.DataFrame({"feature": feature_names[:n], "importance": importance[:n]})
    imp_df = imp_df.sort_values("importance", ascending=False)
    imp_df.to_csv(OUTPUT_DIR / f"{output_prefix}_feature_importance.csv", index=False)

    top = imp_df.head(20).iloc[::-1]
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(top["feature"], top["importance"])
    ax.set_title(f"Top 20 Feature Importance - {output_prefix}")
    ax.set_xlabel("Importance")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f"{output_prefix}_feature_importance_top20.png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    return imp_df


def try_shap_explain(model, X_sample, feature_names: List[str], output_prefix: str) -> str:
    if not RUN_SHAP:
        return "SHAP disabled."
    try:
        import shap
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_sample)
        values = shap_values
        if isinstance(shap_values, list):
            # multi-class: average absolute SHAP across classes
            values = np.mean([np.abs(v) for v in shap_values], axis=0)
        elif getattr(shap_values, "ndim", 0) == 3:
            values = np.mean(np.abs(shap_values), axis=2)
        values = np.asarray(values)
        if hasattr(X_sample, "toarray"):
            X_plot = X_sample.toarray()
        else:
            X_plot = X_sample
        max_features = min(25, len(feature_names))
        shap.summary_plot(values, X_plot, feature_names=feature_names, max_display=max_features, show=False)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / f"{output_prefix}_shap_summary.png", dpi=160, bbox_inches="tight")
        plt.close()
        return "SHAP summary saved."
    except Exception as exc:
        return f"SHAP skipped due to {type(exc).__name__}: {exc}"


def main() -> None:
    print("=" * 80)
    print("PH-05 CLASSIFICATION — AN | AirGlobal Dataset")
    print("=" * 80)

    notes: List[str] = []

    log("\n1️⃣  Loading PH-03 processed features...")
    df, numeric_features, categorical_features = load_processed_data()
    feature_cols = numeric_features + categorical_features
    log(f"  ✅ Dataset: {len(df):,} rows | {len(feature_cols):,} features")
    log(f"  ✅ Numeric features: {len(numeric_features):,} | Categorical features: {len(categorical_features):,}")

    train_df = df[df[SPLIT_COL] == "train"].copy()
    val_df = df[df[SPLIT_COL] == "val"].copy()
    test_df = df[df[SPLIT_COL] == "test"].copy()

    train_df = env_sample(train_df, DEFAULT_MAX_TRAIN_ROWS, TARGET_COL)
    val_df = env_sample(val_df, DEFAULT_MAX_VAL_ROWS, TARGET_COL)
    test_df = env_sample(test_df, DEFAULT_MAX_TEST_ROWS, TARGET_COL)

    log(f"  ✅ Used rows: train={len(train_df):,}, val={len(val_df):,}, test={len(test_df):,}")

    label_encoder = LabelEncoder()
    label_encoder.fit(df[TARGET_COL].astype(str))
    labels = list(label_encoder.classes_)
    with open(OUTPUT_DIR / "label_mapping.json", "w", encoding="utf-8") as f:
        json.dump({int(i): {"label": lab, "label_vi": LABEL_VI.get(lab, lab)} for i, lab in enumerate(labels)}, f, indent=2, ensure_ascii=False)

    X_train_raw = train_df[feature_cols]
    y_train = label_encoder.transform(train_df[TARGET_COL].astype(str))
    X_val_raw = val_df[feature_cols]
    y_val = label_encoder.transform(val_df[TARGET_COL].astype(str))
    X_test_raw = test_df[feature_cols]
    y_test = label_encoder.transform(test_df[TARGET_COL].astype(str))

    log("\n2️⃣  Building preprocessing transformer...")
    preprocessor = build_preprocessor(numeric_features, categorical_features)
    X_train = preprocessor.fit_transform(X_train_raw)
    X_val = preprocessor.transform(X_val_raw)
    X_test = preprocessor.transform(X_test_raw)
    feature_names = get_feature_names(preprocessor, numeric_features, categorical_features)
    log(f"  ✅ Transformed feature matrix: {X_train.shape[1]:,} columns")

    log("\n3️⃣  Optional SMOTE-ENN / class balancing...")
    X_train_bal, y_train_bal, smoteenn_used, smote_notes = maybe_apply_smoteenn(X_train, y_train)
    notes.extend(smote_notes)
    for note in smote_notes:
        log(f"  ⚠️  {note}")
    if not smoteenn_used:
        log("  ✅ SMOTE-ENN not applied; using class_weight/sample_weight where supported.")

    sample_weight_balanced = compute_sample_weight(class_weight="balanced", y=y_train_bal)

    log("\n4️⃣  Training baseline and ensemble models...")
    models: Dict[str, object] = {
        "LogisticRegression_SGD": SGDClassifier(loss="log_loss", max_iter=1000, tol=1e-3, class_weight="balanced", random_state=RANDOM_STATE, n_jobs=-1),
        "DecisionTree": DecisionTreeClassifier(max_depth=18, min_samples_leaf=30, class_weight="balanced", random_state=RANDOM_STATE),
        "RandomForest": RandomForestClassifier(n_estimators=150, max_depth=None, min_samples_leaf=10, class_weight="balanced_subsample", random_state=RANDOM_STATE, n_jobs=-1),
        "ExtraTrees": ExtraTreesClassifier(n_estimators=200, max_depth=None, min_samples_leaf=5, class_weight="balanced", random_state=RANDOM_STATE, n_jobs=-1),
    }
    models.update(get_optional_models(len(labels)))

    tuned_lgbm, optuna_note = tune_lightgbm_with_optuna(X_train_bal, y_train_bal, X_val, y_val, len(labels))
    notes.append(optuna_note)
    if tuned_lgbm is not None:
        models["LightGBM_Optuna"] = tuned_lgbm
        log(f"  ✅ {optuna_note}")
    else:
        log(f"  ⚠️  {optuna_note}")

    trained_models: Dict[str, object] = {}
    metrics_records: List[Dict[str, object]] = []

    for name, model in models.items():
        log(f"  • {name}")
        try:
            if name == "LightGBM_Optuna":
                # Already fitted during tuning.
                fitted = model
            else:
                # Most models already use class_weight. Avoid sample_weight by default because
                # it can slow down linear solvers significantly on sparse matrices.
                fitted = model.fit(X_train_bal, y_train_bal)
            trained_models[name] = fitted
            metrics_records.append(evaluate_model(name, fitted, X_val, y_val, "val"))
            metrics_records.append(evaluate_model(name, fitted, X_test, y_test, "test"))
        except Exception as exc:
            notes.append(f"{name} skipped due to {type(exc).__name__}: {exc}")
            log(f"    ⚠️ skipped: {type(exc).__name__}: {exc}")

    log("\n5️⃣  Training Stacking Ensemble...")
    if TRAIN_STACKING:
        try:
            # Limit stacking training for laptop runtime.
            if len(y_train_bal) > STACKING_MAX_ROWS:
                rng = np.random.default_rng(RANDOM_STATE)
                idx = rng.choice(len(y_train_bal), size=STACKING_MAX_ROWS, replace=False)
                X_stack = X_train_bal[idx]
                y_stack = y_train_bal[idx]
                log(f"  ⚠️  Stacking trained on {STACKING_MAX_ROWS:,} sampled rows for runtime.")
            else:
                X_stack = X_train_bal
                y_stack = y_train_bal

            stack_estimators = []
            for candidate in ["RandomForest", "ExtraTrees", "LightGBM", "XGBoost"]:
                if candidate in trained_models:
                    stack_estimators.append((candidate.lower(), clone(models[candidate])))
            if len(stack_estimators) >= 2:
                stack = StackingClassifier(
                    estimators=stack_estimators,
                    final_estimator=LogisticRegression(max_iter=1000, class_weight="balanced", n_jobs=-1),
                    cv=3,
                    stack_method="predict_proba",
                    n_jobs=-1,
                )
                stack.fit(X_stack, y_stack)
                trained_models["StackingEnsemble"] = stack
                metrics_records.append(evaluate_model("StackingEnsemble", stack, X_val, y_val, "val"))
                metrics_records.append(evaluate_model("StackingEnsemble", stack, X_test, y_test, "test"))
                joblib.dump(stack, MODEL_DIR / "stacking_ensemble_transformed.pkl")
                log("  ✅ Saved: ph05_classification/models/stacking_ensemble_transformed.pkl")
            else:
                notes.append("Stacking skipped because fewer than 2 base models are available.")
                log("  ⚠️  Stacking skipped because fewer than 2 base models are available.")
        except Exception as exc:
            notes.append(f"Stacking skipped due to {type(exc).__name__}: {exc}")
            log(f"  ⚠️  Stacking skipped: {type(exc).__name__}: {exc}")
    else:
        notes.append("Stacking disabled by TRAIN_STACKING=0.")
        log("  ⚠️  Stacking disabled by TRAIN_STACKING=0.")

    log("\n6️⃣  Evaluating and selecting best model by validation Macro F1...")
    metrics_df = pd.DataFrame(metrics_records)
    metrics_df = metrics_df.sort_values(["split", "macro_f1", "weighted_f1"], ascending=[True, False, False])
    metrics_df.to_csv(OUTPUT_DIR / "model_metrics.csv", index=False)

    val_metrics = metrics_df[metrics_df["split"] == "val"].sort_values("macro_f1", ascending=False)
    if val_metrics.empty:
        raise RuntimeError("Không có model nào train/evaluate thành công.")
    best_name = str(val_metrics.iloc[0]["model"])
    best_model = trained_models[best_name]

    test_best_row = metrics_df[(metrics_df["model"] == best_name) & (metrics_df["split"] == "test")].iloc[0]
    print(metrics_df[metrics_df["split"] == "test"].sort_values("macro_f1", ascending=False).to_string(index=False))

    y_test_pred = best_model.predict(X_test)
    report_text = classification_report(y_test, y_test_pred, target_names=labels, zero_division=0)
    with open(OUTPUT_DIR / "classification_report_best_model.txt", "w", encoding="utf-8") as f:
        f.write(f"Best model by validation macro F1: {best_name}\n\n")
        f.write(report_text)

    report_dict = classification_report(y_test, y_test_pred, target_names=labels, output_dict=True, zero_division=0)
    pd.DataFrame(report_dict).transpose().to_csv(OUTPUT_DIR / "classification_report_best_model.csv")
    plot_confusion_matrix(y_test, y_test_pred, labels, OUTPUT_DIR / "confusion_matrix_best_model.png", f"Confusion Matrix - {best_name}")

    log("\n7️⃣  Feature importance / explainability...")
    importance_df = save_feature_importance(best_model, feature_names, "best_model")
    if importance_df is not None:
        log("  ✅ Saved feature importance CSV + top20 PNG")
    else:
        log("  ⚠️  Best model has no built-in feature importance. Skipped.")

    shap_note = "SHAP not attempted."
    if best_name.lower().find("logistic") == -1 and best_name.lower().find("stack") == -1:
        shap_rows = min(SHAP_SAMPLE_ROWS, X_test.shape[0])
        shap_note = try_shap_explain(best_model, X_test[:shap_rows], feature_names, "best_model")
        log(f"  {'✅' if 'saved' in shap_note.lower() else '⚠️'}  {shap_note}")
    else:
        log("  ⚠️  SHAP skipped for non-tree/stacking best model.")
    notes.append(shap_note)

    log("\n8️⃣  Saving production pipeline...")
    production_pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", best_model),
    ])
    joblib.dump(production_pipeline, MODEL_DIR / "best_aqi_classifier_pipeline.pkl")
    joblib.dump(label_encoder, MODEL_DIR / "label_encoder.pkl")
    log("  ✅ Saved: best_aqi_classifier_pipeline.pkl + label_encoder.pkl")

    summary = ModelRunSummary(
        rows_train=int(len(train_df)),
        rows_val=int(len(val_df)),
        rows_test=int(len(test_df)),
        feature_count=int(len(feature_cols)),
        categorical_feature_count=int(len(categorical_features)),
        numeric_feature_count=int(len(numeric_features)),
        best_model_by_val_macro_f1=best_name,
        best_val_macro_f1=float(val_metrics.iloc[0]["macro_f1"]),
        best_test_macro_f1=float(test_best_row["macro_f1"]),
        best_test_weighted_f1=float(test_best_row["weighted_f1"]),
        best_test_accuracy=float(test_best_row["accuracy"]),
        smoteenn_used=bool(smoteenn_used),
        optuna_trials=int(OPTUNA_TRIALS),
        notes=notes,
    )
    with open(OUTPUT_DIR / "model_run_metadata.json", "w", encoding="utf-8") as f:
        json.dump(asdict(summary), f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print("✅ PH-05 DONE")
    print(f"Output folder: {OUTPUT_DIR.relative_to(BASE_DIR)}")
    print(f"Model folder : {MODEL_DIR.relative_to(BASE_DIR)}")
    print(f"Best model   : {best_name}")
    print("=" * 80)


if __name__ == "__main__":
    main()
