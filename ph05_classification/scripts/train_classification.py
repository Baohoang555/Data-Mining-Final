"""
PH-05: Classification Models, Stacking Ensemble & Explainability
Urban Air Quality Intelligence Platform

Nhiệm vụ của An:
- Baseline: Logistic Regression, Decision Tree, Random Forest.
- XGBoost/LightGBM + Optuna tuning nếu thư viện đã cài.
- Stacking Ensemble với base learners tốt nhất + Logistic Regression meta learner.
- SHAP/LIME/PDP/ICE explainability nếu thư viện đã cài; có fallback permutation importance.
- MLflow logging nếu thư viện đã cài; luôn lưu metrics/artifacts ra outputs.

Chạy:
    python ph03_preprocessing/scripts/preprocess_features.py
    python ph05_classification/scripts/train_classification.py
"""

from __future__ import annotations

import json
import os
import pickle
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, StackingClassifier, HistGradientBoostingClassifier
from sklearn.inspection import PartialDependenceDisplay, permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    cohen_kappa_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).resolve().parents[2]
PH03_OUTPUT = BASE_DIR / "ph03_preprocessing" / "outputs"
OUTPUT_DIR = BASE_DIR / "ph05_classification" / "outputs"
MODEL_DIR = BASE_DIR / "ph05_classification" / "models"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
MAX_TRAIN_ROWS = int(os.getenv("MAX_TRAIN_ROWS", "1000"))  # set 0 to use full train set
MAX_VAL_ROWS = int(os.getenv("MAX_VAL_ROWS", "500"))      # set 0 to use full validation set
ENABLE_BOOSTING = os.getenv("ENABLE_BOOSTING", "0") == "1"  # set 1 to run XGBoost/LightGBM
TARGET_COL = "target_aqi_label_next_1h"
LABEL_ORDER = ["Good", "Moderate", "Unhealthy", "Very_Unhealthy", "Hazardous"]


def optional_import(module_name: str):
    try:
        return __import__(module_name)
    except Exception:
        return None


def load_processed_dataset() -> Tuple[pd.DataFrame, List[str]]:
    print("\n1️⃣  Loading PH-03 processed features...")
    csv_path = PH03_OUTPUT / "processed_aqi_features.csv"
    if not csv_path.exists():
        raise FileNotFoundError(
            "Chưa có processed dataset. Hãy chạy: python ph03_preprocessing/scripts/preprocess_features.py"
        )
    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)

    feature_catalog = PH03_OUTPUT / "feature_catalog.csv"
    if feature_catalog.exists():
        feature_cols = pd.read_csv(feature_catalog)["feature"].tolist()
    else:
        non_features = {"timestamp", "station_id", "name", "city", "aqi_label_current", TARGET_COL, "pm25_next_1h", "split"}
        feature_cols = [c for c in df.select_dtypes(include=[np.number, bool]).columns if c not in non_features]

    feature_cols = [c for c in feature_cols if c in df.columns]
    df = df.dropna(subset=[TARGET_COL, "split"])
    for col in feature_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df[feature_cols] = df[feature_cols].replace([np.inf, -np.inf], np.nan).fillna(0)

    print(f"  ✅ Dataset: {len(df):,} rows | {len(feature_cols)} features | {df['station_id'].nunique()} stations")
    return df, feature_cols


def get_splits(df: pd.DataFrame, feature_cols: List[str]):
    encoder = LabelEncoder()
    # Ensure stable class order even when a rare class is absent.
    present = [label for label in LABEL_ORDER if label in set(df[TARGET_COL])]
    other = sorted(set(df[TARGET_COL]) - set(present))
    encoder.fit(present + other)

    X = df[feature_cols]
    y = encoder.transform(df[TARGET_COL])
    split = df["split"].astype(str).values

    data = {
        "X_train": X[split == "train"],
        "y_train": y[split == "train"],
        "X_val": X[split == "val"],
        "y_val": y[split == "val"],
        "X_test": X[split == "test"],
        "y_test": y[split == "test"],
        "encoder": encoder,
    }
    return data


def stratified_sample_xy(X: pd.DataFrame, y: np.ndarray, max_rows: int, name: str) -> Tuple[pd.DataFrame, np.ndarray]:
    if max_rows <= 0 or len(X) <= max_rows:
        return X, y
    y_series = pd.Series(y, index=X.index, name="target")
    sample_parts = []
    # Allocate sample rows proportionally but keep at least 1 row per class when possible.
    for cls, idx in y_series.groupby(y_series).groups.items():
        cls_idx = list(idx)
        n_cls = max(1, int(round(max_rows * len(cls_idx) / len(X))))
        n_cls = min(n_cls, len(cls_idx))
        sample_parts.extend(pd.Series(cls_idx).sample(n_cls, random_state=RANDOM_STATE).tolist())
    if len(sample_parts) > max_rows:
        sample_parts = pd.Series(sample_parts).sample(max_rows, random_state=RANDOM_STATE).tolist()
    sampled_x = X.loc[sample_parts].sort_index()
    sampled_y = y_series.loc[sampled_x.index].values
    print(f"  ⚡ Runtime mode: sampled {name} {len(X):,} → {len(sampled_x):,} rows. Set MAX_{name.upper()}_ROWS=0 for full training.")
    return sampled_x, sampled_y


def apply_runtime_sampling(data: Dict) -> Dict:
    data = dict(data)
    data["X_train"], data["y_train"] = stratified_sample_xy(data["X_train"], data["y_train"], MAX_TRAIN_ROWS, "train")
    data["X_val"], data["y_val"] = stratified_sample_xy(data["X_val"], data["y_val"], MAX_VAL_ROWS, "val")
    return data


def make_pipeline(model) -> Pipeline:
    return Pipeline([
        ("scaler", MinMaxScaler()),
        ("model", model),
    ])


def build_baseline_models() -> Dict[str, Pipeline]:
    return {
        "LogisticRegression": make_pipeline(LogisticRegression(max_iter=120, solver="saga", class_weight="balanced", n_jobs=1, random_state=RANDOM_STATE)),
        "DecisionTree": make_pipeline(DecisionTreeClassifier(max_depth=10, class_weight="balanced", random_state=RANDOM_STATE)),
        "RandomForest": make_pipeline(RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_leaf=2, class_weight="balanced", n_jobs=1, random_state=RANDOM_STATE)),
        "ExtraTrees": make_pipeline(ExtraTreesClassifier(n_estimators=10, max_depth=None, min_samples_leaf=2, class_weight="balanced", n_jobs=1, random_state=RANDOM_STATE)),
    }


def evaluate_model(name: str, model: Pipeline, X, y, encoder: LabelEncoder, split_name: str) -> Dict[str, float]:
    pred = model.predict(X)
    metrics = {
        "model": name,
        "split": split_name,
        "accuracy": float(accuracy_score(y, pred)),
        "weighted_f1": float(f1_score(y, pred, average="weighted", zero_division=0)),
        "macro_f1": float(f1_score(y, pred, average="macro", zero_division=0)),
        "cohen_kappa": float(cohen_kappa_score(y, pred)),
    }
    return metrics


def save_confusion_matrix(name: str, model: Pipeline, X, y, encoder: LabelEncoder, split_name: str = "test") -> None:
    labels = np.arange(len(encoder.classes_))
    pred = model.predict(X)
    cm = confusion_matrix(y, pred, labels=labels)
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(cm, interpolation="nearest")
    ax.figure.colorbar(im, ax=ax)
    ax.set(
        xticks=np.arange(len(encoder.classes_)),
        yticks=np.arange(len(encoder.classes_)),
        xticklabels=encoder.classes_,
        yticklabels=encoder.classes_,
        ylabel="True label",
        xlabel="Predicted label",
        title=f"Confusion Matrix — {name} ({split_name})",
    )
    plt.setp(ax.get_xticklabels(), rotation=35, ha="right", rotation_mode="anchor")
    thresh = cm.max() / 2 if cm.max() else 0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], "d"), ha="center", va="center")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / f"confusion_matrix_{name}_{split_name}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def train_baselines(data, encoder: LabelEncoder) -> Tuple[Dict[str, Pipeline], pd.DataFrame]:
    print("\n2️⃣  Training baseline models...")
    models = build_baseline_models()
    metrics_rows: List[Dict[str, float]] = []

    for name, model in models.items():
        print(f"  • {name}")
        model.fit(data["X_train"], data["y_train"])
        metrics_rows.append(evaluate_model(name, model, data["X_val"], data["y_val"], encoder, "val"))
        metrics_rows.append(evaluate_model(name, model, data["X_test"], data["y_test"], encoder, "test"))
        save_confusion_matrix(name, model, data["X_test"], data["y_test"], encoder)

    metrics = pd.DataFrame(metrics_rows).sort_values(["split", "weighted_f1"], ascending=[True, False])
    metrics.to_csv(OUTPUT_DIR / "baseline_metrics.csv", index=False, encoding="utf-8-sig")
    print("  ✅ Saved: baseline_metrics.csv")
    return models, metrics


def tune_xgboost_if_available(data) -> Optional[Pipeline]:
    if not ENABLE_BOOSTING:
        print("  ⚡ ENABLE_BOOSTING=0 nên bỏ qua XGBoost để chạy nhanh. Set ENABLE_BOOSTING=1 để train thật.")
        return None
    xgb_module = optional_import("xgboost")
    optuna = optional_import("optuna")
    if xgb_module is None:
        print("  ⚠️  xgboost chưa cài. Bỏ qua XGBoost tuning.")
        return None

    XGBClassifier = getattr(xgb_module, "XGBClassifier")
    n_classes = len(np.unique(data["y_train"]))

    if optuna is None:
        print("  ⚠️  optuna chưa cài. Train XGBoost default cấu hình tốt.")
        model = XGBClassifier(
            objective="multi:softprob",
            eval_metric="mlogloss",
            num_class=n_classes,
            n_estimators=10,
            max_depth=5,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=RANDOM_STATE,
            n_jobs=1,
        )
        pipe = make_pipeline(model)
        pipe.fit(data["X_train"], data["y_train"])
        return pipe

    print("\n3️⃣  Tuning XGBoost with Optuna...")
    trial_count = 200
    if len(data["X_train"]) < 5000:
        trial_count = 50

    def objective(trial):
        params = {
            "objective": "multi:softprob",
            "eval_metric": "mlogloss",
            "num_class": n_classes,
            "n_estimators": trial.suggest_int("n_estimators", 100, 1000),
            "max_depth": trial.suggest_int("max_depth", 3, 10),
            "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
            "min_child_weight": trial.suggest_float("min_child_weight", 1e-2, 10.0, log=True),
            "random_state": RANDOM_STATE,
            "n_jobs": -1,
        }
        model = XGBClassifier(**params)
        pipe = make_pipeline(model)
        pipe.fit(data["X_train"], data["y_train"])
        pred = pipe.predict(data["X_val"])
        return f1_score(data["y_val"], pred, average="weighted", zero_division=0)

    pruner = optuna.pruners.HyperbandPruner() if hasattr(optuna, "pruners") else None
    study = optuna.create_study(direction="maximize", pruner=pruner)
    study.optimize(objective, n_trials=trial_count, show_progress_bar=False)

    with open(OUTPUT_DIR / "optuna_xgboost_best_params.json", "w", encoding="utf-8") as f:
        json.dump({"best_value": study.best_value, "best_params": study.best_params}, f, ensure_ascii=False, indent=2)

    best_model = XGBClassifier(
        objective="multi:softprob",
        eval_metric="mlogloss",
        num_class=n_classes,
        random_state=RANDOM_STATE,
        n_jobs=1,
        **study.best_params,
    )
    pipe = make_pipeline(best_model)
    pipe.fit(pd.concat([data["X_train"], data["X_val"]]), np.concatenate([data["y_train"], data["y_val"]]))
    print("  ✅ XGBoost best weighted F1:", round(float(study.best_value), 4))
    return pipe


def tune_lightgbm_if_available(data) -> Optional[Pipeline]:
    if not ENABLE_BOOSTING:
        print("  ⚡ ENABLE_BOOSTING=0 nên bỏ qua LightGBM để chạy nhanh. Set ENABLE_BOOSTING=1 để train thật.")
        return None
    lgb_module = optional_import("lightgbm")
    optuna = optional_import("optuna")
    if lgb_module is None:
        print("  ⚠️  lightgbm chưa cài. Bỏ qua LightGBM tuning.")
        return None

    LGBMClassifier = getattr(lgb_module, "LGBMClassifier")
    if optuna is None:
        model = LGBMClassifier(
            objective="multiclass",
            n_estimators=40,
            learning_rate=0.05,
            num_leaves=31,
            subsample=0.9,
            colsample_bytree=0.9,
            class_weight="balanced",
            random_state=RANDOM_STATE,
            n_jobs=1,
        )
        pipe = make_pipeline(model)
        pipe.fit(data["X_train"], data["y_train"])
        return pipe

    print("\n4️⃣  Tuning LightGBM with Optuna...")
    trial_count = 200
    if len(data["X_train"]) < 5000:
        trial_count = 50

    def objective(trial):
        params = {
            "objective": "multiclass",
            "n_estimators": trial.suggest_int("n_estimators", 100, 1000),
            "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
            "num_leaves": trial.suggest_int("num_leaves", 15, 255),
            "max_depth": trial.suggest_int("max_depth", 3, 12),
            "min_child_samples": trial.suggest_int("min_child_samples", 10, 100),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
            "class_weight": "balanced",
            "random_state": RANDOM_STATE,
            "n_jobs": -1,
            "verbose": -1,
        }
        model = LGBMClassifier(**params)
        pipe = make_pipeline(model)
        pipe.fit(data["X_train"], data["y_train"])
        pred = pipe.predict(data["X_val"])
        return f1_score(data["y_val"], pred, average="weighted", zero_division=0)

    study = optuna.create_study(direction="maximize", pruner=optuna.pruners.HyperbandPruner())
    study.optimize(objective, n_trials=trial_count, show_progress_bar=False)

    with open(OUTPUT_DIR / "optuna_lightgbm_best_params.json", "w", encoding="utf-8") as f:
        json.dump({"best_value": study.best_value, "best_params": study.best_params}, f, ensure_ascii=False, indent=2)

    best_model = LGBMClassifier(
        objective="multiclass",
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=1,
        verbose=-1,
        **study.best_params,
    )
    pipe = make_pipeline(best_model)
    pipe.fit(pd.concat([data["X_train"], data["X_val"]]), np.concatenate([data["y_train"], data["y_val"]]))
    print("  ✅ LightGBM best weighted F1:", round(float(study.best_value), 4))
    return pipe


def train_stacking_ensemble(models: Dict[str, Pipeline], data, tuned_models: Dict[str, Optional[Pipeline]]) -> Pipeline:
    print("\n5️⃣  Training Stacking Ensemble...")
    estimators = []

    if tuned_models.get("XGBoost") is not None:
        estimators.append(("xgb", tuned_models["XGBoost"]))
    if tuned_models.get("LightGBM") is not None:
        estimators.append(("lgbm", tuned_models["LightGBM"]))

    # Use strong sklearn fallback models so the script works even without xgboost/lightgbm.
    estimators.extend([
        ("rf", models["RandomForest"]),
        ("extra", models["ExtraTrees"]),
    ])

    meta = LogisticRegression(max_iter=120, solver="saga", class_weight="balanced", random_state=RANDOM_STATE)
    cv = StratifiedKFold(n_splits=2, shuffle=True, random_state=RANDOM_STATE)
    stack = StackingClassifier(
        estimators=estimators,
        final_estimator=meta,
        stack_method="predict_proba",
        passthrough=False,
        cv=cv,
        n_jobs=1,
    )
    stack.fit(pd.concat([data["X_train"], data["X_val"]]), np.concatenate([data["y_train"], data["y_val"]]))

    with open(MODEL_DIR / "stacking_ensemble.pkl", "wb") as f:
        pickle.dump(stack, f)
    print("  ✅ Saved: ph05_classification/models/stacking_ensemble.pkl")
    return stack


def save_classification_reports(models: Dict[str, Pipeline], stack, data, encoder: LabelEncoder) -> pd.DataFrame:
    print("\n6️⃣  Evaluating final models on test set...")
    rows = []
    all_models = dict(models)
    all_models["StackingEnsemble"] = stack

    for name, model in all_models.items():
        metrics = evaluate_model(name, model, data["X_test"], data["y_test"], encoder, "test")
        rows.append(metrics)
        save_confusion_matrix(name, model, data["X_test"], data["y_test"], encoder, "test")
        report = classification_report(
            data["y_test"],
            model.predict(data["X_test"]),
            target_names=encoder.classes_,
            zero_division=0,
            output_dict=True,
        )
        pd.DataFrame(report).T.to_csv(OUTPUT_DIR / f"classification_report_{name}.csv", encoding="utf-8-sig")

    metrics = pd.DataFrame(rows).sort_values("weighted_f1", ascending=False)
    metrics.to_csv(OUTPUT_DIR / "final_model_metrics.csv", index=False, encoding="utf-8-sig")
    print(metrics.to_string(index=False))
    return metrics


def explain_with_permutation(model, data, feature_cols: List[str]) -> pd.DataFrame:
    print("\n7️⃣  Feature importance / explainability...")
    sample_x = data["X_test"].sample(min(800, len(data["X_test"])), random_state=RANDOM_STATE)
    y_test_series = pd.Series(data["y_test"], index=data["X_test"].index)
    sample_y = y_test_series.loc[sample_x.index].values
    result = permutation_importance(
        model,
        sample_x,
        sample_y,
        n_repeats=3,
        random_state=RANDOM_STATE,
        scoring="f1_weighted",
        n_jobs=1,
    )
    importance = pd.DataFrame({
        "feature": feature_cols,
        "importance_mean": result.importances_mean,
        "importance_std": result.importances_std,
    }).sort_values("importance_mean", ascending=False)
    importance.to_csv(OUTPUT_DIR / "permutation_importance.csv", index=False, encoding="utf-8-sig")

    top = importance.head(20).iloc[::-1]
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.barh(top["feature"], top["importance_mean"])
    ax.set_xlabel("Mean decrease in weighted F1")
    ax.set_title("Top 20 Feature Importance — Permutation")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "permutation_importance_top20.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  ✅ Saved: permutation_importance.csv + permutation_importance_top20.png")
    return importance


def explain_with_shap_if_available(tree_pipeline, data, feature_cols: List[str], encoder: LabelEncoder) -> None:
    shap = optional_import("shap")
    if shap is None:
        print("  ⚠️  shap chưa cài. Đã dùng permutation importance fallback.")
        return
    try:
        # Use a tree base learner for SHAP to keep runtime practical. Stacking itself is still explained
        # by permutation importance, while this plot shows the strongest tree learner's global feature effects.
        if not isinstance(tree_pipeline, Pipeline) or "model" not in tree_pipeline.named_steps:
            print("  ⚠️  Không tìm thấy tree pipeline phù hợp cho SHAP.")
            return
        sample = data["X_test"].sample(min(150, len(data["X_test"])), random_state=RANDOM_STATE)
        scaler = tree_pipeline.named_steps.get("scaler")
        tree_model = tree_pipeline.named_steps["model"]
        sample_scaled = scaler.transform(sample) if scaler is not None else sample.values
        explainer = shap.TreeExplainer(tree_model)
        shap_values = explainer.shap_values(sample_scaled)
        # For multiclass, use the mean absolute SHAP by class if needed.
        if isinstance(shap_values, list):
            values_for_plot = np.mean(np.abs(np.stack(shap_values, axis=0)), axis=0)
        else:
            values_for_plot = shap_values
        shap.summary_plot(values_for_plot, sample, feature_names=feature_cols, show=False, max_display=20)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "shap_summary_beeswarm_tree_base.png", dpi=150, bbox_inches="tight")
        plt.close()
        print("  ✅ Saved: shap_summary_beeswarm_tree_base.png")
    except Exception as exc:
        print(f"  ⚠️  SHAP bị lỗi ({exc.__class__.__name__}). Bỏ qua SHAP plot.")


def explain_with_lime_if_available(model, data, feature_cols: List[str], encoder: LabelEncoder) -> None:
    lime = optional_import("lime")
    if lime is None:
        print("  ⚠️  lime chưa cài. Bỏ qua LIME.")
        return
    try:
        from lime.lime_tabular import LimeTabularExplainer
        explainer = LimeTabularExplainer(
            training_data=data["X_train"].values,
            feature_names=feature_cols,
            class_names=encoder.classes_.tolist(),
            mode="classification",
            discretize_continuous=True,
            random_state=RANDOM_STATE,
        )
        rows = []
        # Pick one sample per predicted/true class when possible.
        test_df = data["X_test"].copy()
        test_df["_y"] = data["y_test"]
        selected_indices = []
        for cls in np.unique(data["y_test"]):
            matches = test_df[test_df["_y"] == cls]
            if not matches.empty:
                selected_indices.append(matches.index[0])
        selected_indices = selected_indices[:5]

        for idx in selected_indices:
            x = data["X_test"].loc[idx].values
            exp = explainer.explain_instance(x, model.predict_proba, num_features=10)
            html_path = OUTPUT_DIR / f"lime_explanation_idx_{idx}.html"
            exp.save_to_file(str(html_path))
            rows.append({"sample_index": int(idx), "true_label": encoder.inverse_transform([int(test_df.loc[idx, "_y"])] )[0], "file": html_path.name})
        pd.DataFrame(rows).to_csv(OUTPUT_DIR / "lime_explanation_index.csv", index=False, encoding="utf-8-sig")
        print("  ✅ Saved LIME html explanations")
    except Exception as exc:
        print(f"  ⚠️  LIME bị lỗi ({exc.__class__.__name__}). Bỏ qua.")


def save_pdp_ice(model, data, feature_importance: pd.DataFrame) -> None:
    print("\n8️⃣  PDP & ICE plots...")
    top_features = [f for f in feature_importance["feature"].head(3).tolist() if f in data["X_test"].columns]
    if not top_features:
        print("  ⚠️  Không có top features để vẽ PDP/ICE.")
        return

    sample = data["X_test"].sample(min(150, len(data["X_test"])), random_state=RANDOM_STATE)
    # PDP for top features, one figure each to avoid clutter.
    for feature in top_features:
        try:
            fig, ax = plt.subplots(figsize=(7, 5))
            PartialDependenceDisplay.from_estimator(
                model,
                sample,
                features=[feature],
                kind="both",
                target=0,
                subsample=min(50, len(sample)),
                random_state=RANDOM_STATE,
                ax=ax,
            )
            ax.set_title(f"PDP & ICE — {feature}")
            fig.tight_layout()
            fig.savefig(OUTPUT_DIR / f"pdp_ice_{feature}.png", dpi=150, bbox_inches="tight")
            plt.close(fig)
        except Exception as exc:
            print(f"  ⚠️  Bỏ qua PDP/ICE {feature}: {exc.__class__.__name__}")
    print("  ✅ Saved PDP/ICE plots for top features")


def log_mlflow_if_available(final_metrics: pd.DataFrame, params: Dict) -> None:
    mlflow = optional_import("mlflow")
    if mlflow is None:
        with open(OUTPUT_DIR / "mlflow_fallback_log.json", "w", encoding="utf-8") as f:
            json.dump({"params": params, "metrics": final_metrics.to_dict("records")}, f, ensure_ascii=False, indent=2)
        print("  ⚠️  mlflow chưa cài. Đã lưu fallback log JSON.")
        return

    try:
        mlflow.set_experiment("Urban_AQI_Classification")
        best = final_metrics.iloc[0].to_dict()
        with mlflow.start_run(run_name="stacking_ensemble_an"):
            mlflow.log_params(params)
            for k, v in best.items():
                if isinstance(v, (int, float)):
                    mlflow.log_metric(k, float(v))
            mlflow.log_artifacts(str(OUTPUT_DIR))
            mlflow.log_artifact(str(MODEL_DIR / "stacking_ensemble.pkl"))
        print("  ✅ MLflow run logged.")
    except Exception as exc:
        print(f"  ⚠️  MLflow logging lỗi ({exc.__class__.__name__}).")


def save_label_encoder_and_features(encoder: LabelEncoder, feature_cols: List[str]) -> None:
    with open(MODEL_DIR / "label_encoder.pkl", "wb") as f:
        pickle.dump(encoder, f)
    with open(MODEL_DIR / "feature_columns.json", "w", encoding="utf-8") as f:
        json.dump(feature_cols, f, ensure_ascii=False, indent=2)


def main() -> None:
    print("=" * 80)
    print("PH-05 CLASSIFICATION — AN")
    print("=" * 80)

    df, feature_cols = load_processed_dataset()
    data = apply_runtime_sampling(get_splits(df, feature_cols))
    encoder = data["encoder"]
    save_label_encoder_and_features(encoder, feature_cols)

    models, baseline_metrics = train_baselines(data, encoder)

    tuned_models = {
        "XGBoost": tune_xgboost_if_available(data),
        "LightGBM": tune_lightgbm_if_available(data),
    }
    for name, model in tuned_models.items():
        if model is not None:
            save_confusion_matrix(name, model, data["X_test"], data["y_test"], encoder)
            row = evaluate_model(name, model, data["X_test"], data["y_test"], encoder, "test")
            pd.DataFrame([row]).to_csv(OUTPUT_DIR / f"{name.lower()}_metrics.csv", index=False, encoding="utf-8-sig")
            models[name] = model

    stack = train_stacking_ensemble(models, data, tuned_models)
    final_metrics = save_classification_reports(models, stack, data, encoder)
    importance = explain_with_permutation(stack, data, feature_cols)
    explain_with_shap_if_available(models.get("RandomForest", stack), data, feature_cols, encoder)
    explain_with_lime_if_available(stack, data, feature_cols, encoder)
    save_pdp_ice(stack, data, importance)
    log_mlflow_if_available(final_metrics, {
        "target": TARGET_COL,
        "feature_count": len(feature_cols),
        "base_learners": "XGBoost/LightGBM when ENABLE_BOOSTING=1 + RandomForest + ExtraTrees",
        "meta_learner": "LogisticRegression",
        "split_strategy": "PH-03 temporal test + stratified train/val",
    })

    print("\n" + "=" * 80)
    print("✅ PH-05 DONE")
    print("Output folder:", OUTPUT_DIR.relative_to(BASE_DIR))
    print("Model folder :", MODEL_DIR.relative_to(BASE_DIR))
    print("=" * 80)


if __name__ == "__main__":
    main()
