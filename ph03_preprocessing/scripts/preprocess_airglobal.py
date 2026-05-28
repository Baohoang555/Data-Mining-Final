"""
PH-03: Data Preprocessing & Feature Engineering — AirGlobal AQI Dataset
Author: An

Pipeline chính:
1) Đọc dữ liệu từ data/raw/global_air_quality_2014_2025.csv hoặc datalake parquet.
2) Chuẩn hóa tên cột, kiểu dữ liệu, ngày tháng và target label.
3) Xử lý duplicate, giá trị thiếu, giá trị ngoài giới hạn vật lý và outlier bằng IQR/winsorization.
4) Feature engineering: thời gian, chu kỳ, pollutant ratios, environmental interaction,
   city/country frequency, lag/rolling theo chuỗi thời gian của từng city.
5) Chia train/validation/test theo thời gian để giảm data leakage.
6) Xuất processed dataset + reports cho PH-05.

Chạy từ thư mục gốc project:
    python ph03_preprocessing/scripts/preprocess_airglobal.py
"""

from __future__ import annotations

import json
import math
import os
import re
import warnings
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_CSV = BASE_DIR / "data" / "raw" / "global_air_quality_2014_2025.csv"
DATALAKE_DIR = BASE_DIR / "data" / "datalake" / "aqi"
OUTPUT_DIR = BASE_DIR / "ph03_preprocessing" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SAVE_FULL_CSV = os.getenv("SAVE_FULL_CSV", "0") == "1"
SAVE_PARQUET = os.getenv("SAVE_PARQUET", "0") == "1"

RANDOM_STATE = 42
TARGET_COL = "target_aqi_bucket"
DATE_COL = "date"
SPLIT_COL = "split"

# AQI numeric value is intentionally excluded from ML features because AQI_Bucket is derived from AQI.
LEAKAGE_COLUMNS = {"aqi", "aqi_bucket", "aqi_bucket_clean", TARGET_COL}

COLUMN_RENAME = {
    "Country": "country",
    "State": "state",
    "City": "city",
    "Date": "date",
    "PM2.5 (ug/m3)": "pm25",
    "PM10 (ug/m3)": "pm10",
    "NO (ug/m3)": "no",
    "NO2 (ug/m3)": "no2",
    "NOx (ppb)": "nox",
    "NH3 (ug/m3)": "nh3",
    "CO (mg/m3)": "co",
    "SO2 (ug/m3)": "so2",
    "O3 (ug/m3)": "o3",
    "Benzene (ug/m3)": "benzene",
    "Toluene (ug/m3)": "toluene",
    "Xylene (ug/m3)": "xylene",
    "AQI": "aqi",
    "AQI_Bucket": "aqi_bucket",
    "Wind_Speed (km/h)": "wind_speed",
    "Humidity (%)": "humidity",
    "Deforestation_Rate_%": "deforestation_rate",
    "Industry_Growth_%": "industry_growth",
    "CO2_Emission_MT": "co2_emission",
    "Population_Density_per_SqKm": "population_density",
    "Division": "division",
    "Province": "province",
    "Region": "region",
    "Prefecture": "prefecture",
    "Federal_District": "federal_district",
    "year": "year",
}

POLLUTANT_COLS = [
    "pm25", "pm10", "no", "no2", "nox", "nh3", "co", "so2", "o3",
    "benzene", "toluene", "xylene",
]
ENV_COLS = [
    "wind_speed", "humidity", "deforestation_rate", "industry_growth",
    "co2_emission", "population_density",
]
NUMERIC_BASE_COLS = POLLUTANT_COLS + ENV_COLS
CATEGORICAL_BASE_COLS = [
    "country", "state", "city", "division", "province", "region", "prefecture", "federal_district",
]

# Conservative sanity ranges. Values outside these ranges are treated as sensor/data-entry errors.
PHYSICAL_LIMITS = {
    "pm25": (0, 1500),
    "pm10": (0, 2500),
    "no": (0, 2000),
    "no2": (0, 2000),
    "nox": (0, 4000),
    "nh3": (0, 2000),
    "co": (0, 100),
    "so2": (0, 2000),
    "o3": (0, 2000),
    "benzene": (0, 500),
    "toluene": (0, 1000),
    "xylene": (0, 1000),
    "aqi": (0, 1000),
    "wind_speed": (0, 300),
    "humidity": (0, 100),
    "deforestation_rate": (0, 100),
    "industry_growth": (-100, 300),
    "co2_emission": (0, 100000),
    "population_density": (0, 200000),
}

AQI_NUMERIC_THRESHOLDS = [50, 100, 200, 300, 400]
AQI_NUMERIC_LABELS = ["Good", "Satisfactory", "Moderate", "Unhealthy", "Very_Unhealthy", "Hazardous"]

LABEL_NORMALIZATION = {
    "excellent": "Good",
    "good": "Good",
    "satisfactory": "Satisfactory",
    "lightly polluted": "Satisfactory",
    "moderate": "Moderate",
    "moderately polluted": "Moderate",
    "unhealthy for sensitive groups": "Unhealthy",
    "unhealthy": "Unhealthy",
    "poor": "Unhealthy",
    "heavily polluted": "Unhealthy",
    "very poor": "Very_Unhealthy",
    "very unhealthy": "Very_Unhealthy",
    "severe": "Hazardous",
    "severely polluted": "Hazardous",
    "hazardous": "Hazardous",
    "unknown": np.nan,
    "nan": np.nan,
    "none": np.nan,
    "": np.nan,
}

LABEL_VI = {
    "Good": "Tốt",
    "Satisfactory": "Khá / Chấp nhận được",
    "Moderate": "Trung bình",
    "Unhealthy": "Kém / Không lành mạnh",
    "Very_Unhealthy": "Rất xấu",
    "Hazardous": "Nguy hại",
}

LAG_PERIODS = [1, 3, 12]        # Dataset mới là daily/monthly-level, nên dùng lag theo period thay vì lag theo giờ.
ROLLING_WINDOWS = [3, 12]
ENABLE_ROLLING_FEATURES = os.getenv("ENABLE_ROLLING_FEATURES", "0") == "1"
LAG_BASE_COLS = ["pm25", "pm10", "no2", "o3", "co", "humidity", "wind_speed"]


@dataclass
class PreprocessSummary:
    raw_rows_loaded: int
    rows_after_cleaning: int
    duplicate_rows_removed: int
    countries: int
    cities: int
    date_from: str
    date_to: str
    numeric_features: int
    categorical_features: int
    total_features: int
    target_col: str
    label_distribution: Dict[str, int]
    split_distribution: Dict[str, int]
    notes: List[str]


def log(msg: str) -> None:
    print(msg, flush=True)


def normalize_column_name(col: str) -> str:
    col = col.strip()
    if col in COLUMN_RENAME:
        return COLUMN_RENAME[col]
    col = re.sub(r"[^0-9a-zA-Z]+", "_", col).strip("_").lower()
    return col


def read_raw_or_datalake() -> pd.DataFrame:
    """Read datalake parquet if possible, otherwise fallback to raw CSV."""
    notes: List[str] = []
    parquet_files = list(DATALAKE_DIR.rglob("*.parquet")) if DATALAKE_DIR.exists() else []

    if parquet_files:
        try:
            log(f"  Found {len(parquet_files):,} parquet files in datalake. Reading...")
            frames = []
            for idx, fp in enumerate(parquet_files, start=1):
                try:
                    frames.append(pd.read_parquet(fp))
                except Exception as exc:
                    # If pyarrow/fastparquet is missing, the first read usually fails.
                    raise RuntimeError(f"Cannot read parquet: {exc}") from exc
                if idx % 5000 == 0:
                    log(f"    Read {idx:,}/{len(parquet_files):,} parquet files...")
            df = pd.concat(frames, ignore_index=True)
            log(f"  ✅ Loaded datalake parquet: {len(df):,} rows")
            return df
        except Exception as exc:
            log(f"  ⚠️  Không đọc được datalake parquet ({type(exc).__name__}). Fallback sang raw CSV.")
            notes.append(str(exc))

    if not RAW_CSV.exists():
        raise FileNotFoundError(
            f"Không tìm thấy dữ liệu. Cần có {RAW_CSV} hoặc parquet trong {DATALAKE_DIR}."
        )
    df = pd.read_csv(RAW_CSV)
    log(f"  ✅ Loaded raw CSV: {len(df):,} rows")
    return df


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [normalize_column_name(c) for c in df.columns]
    return df


def normalize_label(value) -> object:
    if pd.isna(value):
        return np.nan
    key = str(value).strip().lower().replace("_", " ")
    return LABEL_NORMALIZATION.get(key, str(value).strip().replace(" ", "_"))


def derive_label_from_aqi(aqi_value) -> object:
    if pd.isna(aqi_value):
        return np.nan
    try:
        val = float(aqi_value)
    except Exception:
        return np.nan
    for threshold, label in zip(AQI_NUMERIC_THRESHOLDS, AQI_NUMERIC_LABELS):
        if val <= threshold:
            return label
    return "Hazardous"


def add_target_label(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "aqi_bucket" in df.columns:
        df["aqi_bucket_clean"] = df["aqi_bucket"].apply(normalize_label)
    else:
        df["aqi_bucket_clean"] = np.nan

    if "aqi" in df.columns:
        derived = df["aqi"].apply(derive_label_from_aqi)
        df[TARGET_COL] = df["aqi_bucket_clean"].fillna(derived)
    else:
        df[TARGET_COL] = df["aqi_bucket_clean"]

    df = df.dropna(subset=[TARGET_COL])
    df = df[df[TARGET_COL].isin(AQI_NUMERIC_LABELS)]
    return df


def clean_base_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, int, pd.DataFrame]:
    df = standardize_columns(df)

    required = ["country", "city", "date"]
    missing_required = [c for c in required if c not in df.columns]
    if missing_required:
        raise ValueError(f"Dataset thiếu cột bắt buộc: {missing_required}")

    df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
    df = df.dropna(subset=[DATE_COL, "country", "city"])

    # Normalize categorical text values.
    for col in CATEGORICAL_BASE_COLS:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip().replace({"": pd.NA}).fillna("Unknown")

    # Convert numeric columns.
    for col in set(NUMERIC_BASE_COLS + ["aqi"]):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    before_dups = len(df)
    subset = [c for c in ["country", "state", "city", "date"] if c in df.columns]
    df = df.drop_duplicates(subset=subset, keep="first")
    duplicate_rows_removed = before_dups - len(df)

    # Physical validity check.
    invalid_records = []
    for col, (lo, hi) in PHYSICAL_LIMITS.items():
        if col not in df.columns:
            continue
        mask = df[col].notna() & ((df[col] < lo) | (df[col] > hi))
        invalid_count = int(mask.sum())
        if invalid_count > 0:
            invalid_records.append({"column": col, "invalid_count": invalid_count, "min_allowed": lo, "max_allowed": hi})
            df.loc[mask, col] = np.nan

    invalid_report = pd.DataFrame(invalid_records)
    return df, duplicate_rows_removed, invalid_report


def save_missing_report(df: pd.DataFrame, filename: str = "missing_report_before_imputation.csv") -> pd.DataFrame:
    report = []
    for col in df.columns:
        missing = int(df[col].isna().sum())
        report.append({
            "column": col,
            "missing_count": missing,
            "missing_pct": round(missing / max(len(df), 1) * 100, 4),
            "dtype": str(df[col].dtype),
        })
    out = pd.DataFrame(report).sort_values("missing_pct", ascending=False)
    out.to_csv(OUTPUT_DIR / filename, index=False)
    return out


def impute_numeric_by_hierarchy(df: pd.DataFrame, numeric_cols: List[str]) -> pd.DataFrame:
    df = df.copy()
    for col in numeric_cols:
        if col not in df.columns:
            continue
        # Fill by country-city median, then country median, then global median.
        city_median = df.groupby(["country", "city"])[col].transform("median")
        country_median = df.groupby("country")[col].transform("median")
        global_median = df[col].median()
        if pd.isna(global_median):
            global_median = 0.0
        df[col] = df[col].fillna(city_median).fillna(country_median).fillna(global_median)
    return df


def winsorize_iqr(df: pd.DataFrame, numeric_cols: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """IQR outlier treatment by country when possible; clip instead of dropping rows."""
    df = df.copy()
    records = []
    for col in numeric_cols:
        if col not in df.columns:
            continue
        total_outliers = 0
        for country, idx in df.groupby("country").groups.items():
            values = df.loc[idx, col].dropna()
            if len(values) < 30:
                continue
            q1 = values.quantile(0.25)
            q3 = values.quantile(0.75)
            iqr = q3 - q1
            if not np.isfinite(iqr) or iqr <= 0:
                continue
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            mask = (df.loc[idx, col] < lower) | (df.loc[idx, col] > upper)
            count = int(mask.sum())
            if count:
                total_outliers += count
                df.loc[idx, col] = df.loc[idx, col].clip(lower=lower, upper=upper)
        records.append({"column": col, "outlier_count_clipped": total_outliers})
    report = pd.DataFrame(records).sort_values("outlier_count_clipped", ascending=False)
    return df, report


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["year"] = df[DATE_COL].dt.year
    df["month"] = df[DATE_COL].dt.month
    df["quarter"] = df[DATE_COL].dt.quarter
    df["day_of_year"] = df[DATE_COL].dt.dayofyear
    df["decade"] = (df["year"] // 10) * 10
    df["is_covid_period"] = df["year"].isin([2020, 2021]).astype(int)

    def season_from_month(m: int) -> str:
        if m in [12, 1, 2]:
            return "Winter"
        if m in [3, 4, 5]:
            return "Spring"
        if m in [6, 7, 8]:
            return "Summer"
        return "Autumn"

    df["season"] = df["month"].apply(season_from_month)
    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
    df["doy_sin"] = np.sin(2 * np.pi * df["day_of_year"] / 365.25)
    df["doy_cos"] = np.cos(2 * np.pi * df["day_of_year"] / 365.25)
    return df


def safe_div(numerator: pd.Series, denominator: pd.Series, eps: float = 1e-6) -> pd.Series:
    return numerator / (denominator.replace(0, np.nan) + eps)


def add_domain_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Ratios among pollutants. These are useful because AQI category often depends on relative pollutant severity.
    if {"pm25", "pm10"}.issubset(df.columns):
        df["pm25_pm10_ratio"] = safe_div(df["pm25"], df["pm10"])
        df["pm10_minus_pm25"] = df["pm10"] - df["pm25"]
    if {"no2", "nox"}.issubset(df.columns):
        df["no2_nox_ratio"] = safe_div(df["no2"], df["nox"])
    if {"benzene", "toluene"}.issubset(df.columns):
        df["benzene_toluene_ratio"] = safe_div(df["benzene"], df["toluene"])
    if {"so2", "no2"}.issubset(df.columns):
        df["so2_no2_ratio"] = safe_div(df["so2"], df["no2"])

    # Interactions with environmental/social variables.
    if {"pm25", "humidity"}.issubset(df.columns):
        df["pm25_humidity_interaction"] = df["pm25"] * df["humidity"]
        df["high_humidity_flag"] = (df["humidity"] >= 80).astype(int)
    if {"pm25", "wind_speed"}.issubset(df.columns):
        df["pm25_wind_dispersion"] = df["pm25"] / (df["wind_speed"] + 1)
        df["low_wind_flag"] = (df["wind_speed"] < 5).astype(int)
    if {"population_density", "industry_growth"}.issubset(df.columns):
        df["industry_density_interaction"] = df["population_density"] * df["industry_growth"]
    if {"co2_emission", "population_density"}.issubset(df.columns):
        df["co2_per_density"] = df["co2_emission"] / (df["population_density"] + 1)

    # Frequency encoding for geographical identifiers. This avoids creating thousands of dense dummy columns in PH-03.
    n = max(len(df), 1)
    for col in ["country", "city", "state"]:
        if col in df.columns:
            freq = df[col].value_counts(normalize=True)
            df[f"{col}_freq"] = df[col].map(freq).fillna(0)

    if {"country", "city"}.issubset(df.columns):
        city_key = df["country"].astype(str) + "__" + df["city"].astype(str)
        freq = city_key.value_counts(normalize=True)
        df["country_city_freq"] = city_key.map(freq).fillna(0)

    return df


def add_lag_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create compact lag features by country-city time series.

    For a 1M+ row dataset, lag features are useful and fast. Rolling features are
    optional because group rolling over thousands of cities can be slow on normal
    laptops. To enable rolling means, set ENABLE_ROLLING_FEATURES=1.
    """
    df = df.copy().sort_values(["country", "city", DATE_COL])
    group_cols = ["country", "city"]
    valid_cols = [c for c in LAG_BASE_COLS if c in df.columns]

    for col in valid_cols:
        grouped_col = df.groupby(group_cols, sort=False)[col]
        for lag in LAG_PERIODS:
            new_col = f"{col}_lag_{lag}"
            df[new_col] = grouped_col.shift(lag)
            # First records of a city have no history; fill with current value as neutral fallback.
            df[new_col] = df[new_col].fillna(df[col])

        if ENABLE_ROLLING_FEATURES:
            for window in ROLLING_WINDOWS:
                new_col = f"{col}_roll_mean_{window}"
                df[new_col] = grouped_col.transform(
                    lambda s: s.shift(1).rolling(window=window, min_periods=1).mean()
                )
                df[new_col] = df[new_col].fillna(df[col])

    return df

def split_temporally(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().sort_values(DATE_COL)
    unique_dates = np.array(sorted(df[DATE_COL].dropna().unique()))
    if len(unique_dates) < 5:
        # Fallback if date granularity is too low.
        rng = np.random.default_rng(RANDOM_STATE)
        rand = rng.random(len(df))
        df[SPLIT_COL] = np.where(rand < 0.7, "train", np.where(rand < 0.85, "val", "test"))
        return df

    train_cut = unique_dates[int(len(unique_dates) * 0.70)]
    val_cut = unique_dates[int(len(unique_dates) * 0.85)]

    df[SPLIT_COL] = "test"
    df.loc[df[DATE_COL] < train_cut, SPLIT_COL] = "train"
    df.loc[(df[DATE_COL] >= train_cut) & (df[DATE_COL] < val_cut), SPLIT_COL] = "val"

    # Guard against a rare missing class in train due temporal split.
    if df.loc[df[SPLIT_COL] == "train", TARGET_COL].nunique() < 2:
        log("  ⚠️  Temporal split produced too few train classes. Fallback to stratified-like random split.")
        rng = np.random.default_rng(RANDOM_STATE)
        rand = rng.random(len(df))
        df[SPLIT_COL] = np.where(rand < 0.7, "train", np.where(rand < 0.85, "val", "test"))
    return df


def build_feature_catalog(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str], List[str]]:
    excluded = set([DATE_COL, SPLIT_COL, TARGET_COL, "aqi", "aqi_bucket", "aqi_bucket_clean"])
    feature_cols = [c for c in df.columns if c not in excluded]

    categorical_features = [
        c for c in feature_cols
        if str(df[c].dtype) in ["object", "string", "category"]
    ]
    numeric_features = [c for c in feature_cols if c not in categorical_features]

    catalog_records = []
    for col in feature_cols:
        if col in categorical_features:
            group = "categorical/geography"
        elif any(token in col for token in ["lag", "roll"]):
            group = "lag_rolling"
        elif col in ["year", "month", "quarter", "day_of_year", "decade", "month_sin", "month_cos", "doy_sin", "doy_cos", "is_covid_period"]:
            group = "time"
        elif any(token in col for token in ["ratio", "interaction", "flag", "dispersion", "freq", "density"]):
            group = "domain_engineered"
        else:
            group = "base_numeric"
        catalog_records.append({
            "feature": col,
            "dtype": str(df[col].dtype),
            "feature_type": "categorical" if col in categorical_features else "numeric",
            "feature_group": group,
            "missing_count": int(df[col].isna().sum()),
        })
    catalog = pd.DataFrame(catalog_records)
    return catalog, numeric_features, categorical_features


def main() -> None:
    print("=" * 80)
    print("PH-03 PREPROCESSING — AN | AirGlobal Dataset")
    print("=" * 80)

    notes: List[str] = []

    log("\n1️⃣  Loading dataset...")
    raw_df = read_raw_or_datalake()
    raw_rows = len(raw_df)

    log("\n2️⃣  Cleaning schema, dates, duplicates, physical invalid values...")
    df, duplicate_removed, invalid_report = clean_base_data(raw_df)
    invalid_report.to_csv(OUTPUT_DIR / "physical_invalid_values_report.csv", index=False)
    log(f"  ✅ After basic cleaning: {len(df):,} rows | duplicates removed: {duplicate_removed:,}")

    log("\n3️⃣  Creating target label and avoiding AQI leakage...")
    df = add_target_label(df)
    log(f"  ✅ Rows with valid target: {len(df):,} | classes: {df[TARGET_COL].nunique()}")

    log("\n4️⃣  Missing pattern report before imputation...")
    missing_before = int(df.isna().sum().sum())
    missing_report = save_missing_report(df)
    log(f"  ✅ Missing cells before imputation: {missing_before:,}")

    existing_numeric_cols = [c for c in NUMERIC_BASE_COLS if c in df.columns]

    log("\n5️⃣  IQR outlier treatment + hierarchical median imputation...")
    df, outlier_report = winsorize_iqr(df, existing_numeric_cols)
    outlier_report.to_csv(OUTPUT_DIR / "outlier_iqr_report.csv", index=False)
    df = impute_numeric_by_hierarchy(df, existing_numeric_cols)
    missing_after_base = int(df[existing_numeric_cols].isna().sum().sum()) if existing_numeric_cols else 0
    log(f"  ✅ Missing numeric base cells after imputation: {missing_after_base:,}")

    log("\n6️⃣  Feature engineering: time, ratios, interactions, lag/rolling...")
    df = add_time_features(df)
    df = add_domain_features(df)
    df = add_lag_rolling_features(df)

    # Final cleanup for infinite values and residual missing in numeric engineered columns.
    numeric_cols_now = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    df[numeric_cols_now] = df[numeric_cols_now].replace([np.inf, -np.inf], np.nan)
    # Fast final fallback for engineered features. Base numeric columns already used hierarchical imputation.
    numeric_medians = df[numeric_cols_now].median(numeric_only=True)
    df[numeric_cols_now] = df[numeric_cols_now].fillna(numeric_medians).fillna(0)
    for col in CATEGORICAL_BASE_COLS + ["season"]:
        if col in df.columns:
            df[col] = df[col].astype("string").fillna("Unknown")

    log("\n7️⃣  Temporal train/validation/test split...")
    df = split_temporally(df)

    catalog, numeric_features, categorical_features = build_feature_catalog(df)
    catalog.to_csv(OUTPUT_DIR / "feature_catalog.csv", index=False)

    label_dist = df[TARGET_COL].value_counts().reindex(AQI_NUMERIC_LABELS).fillna(0).astype(int)
    label_dist_df = pd.DataFrame({
        "label": label_dist.index,
        "label_vi": [LABEL_VI.get(x, x) for x in label_dist.index],
        "rows": label_dist.values,
        "pct": np.round(label_dist.values / max(label_dist.values.sum(), 1) * 100, 4),
    })
    label_dist_df.to_csv(OUTPUT_DIR / "label_distribution.csv", index=False)

    split_summary = df[SPLIT_COL].value_counts().reindex(["train", "val", "test"]).fillna(0).astype(int)
    split_summary_df = pd.DataFrame({"split": split_summary.index, "rows": split_summary.values})
    split_summary_df.to_csv(OUTPUT_DIR / "split_summary.csv", index=False)

    date_from = str(df[DATE_COL].min().date()) if not df.empty else ""
    date_to = str(df[DATE_COL].max().date()) if not df.empty else ""

    log(f"  ✅ Split: {split_summary_df.to_dict(orient='records')}")
    log(f"  ✅ Features: {len(numeric_features)} numeric + {len(categorical_features)} categorical = {len(numeric_features) + len(categorical_features)}")

    log("\n8️⃣  Saving processed dataset and metadata...")
    # Save date as ISO string for portable outputs. Pickle is the default full output because
    # it is much faster than writing a 1M+ row CSV on normal laptops.
    df[DATE_COL] = pd.to_datetime(df[DATE_COL]).dt.strftime("%Y-%m-%d")
    processed_pkl = OUTPUT_DIR / "processed_airglobal_features.pkl"
    df.to_pickle(processed_pkl)
    df.head(5000).to_csv(OUTPUT_DIR / "processed_airglobal_sample_5000.csv", index=False)

    if SAVE_FULL_CSV:
        processed_csv = OUTPUT_DIR / "processed_airglobal_features.csv"
        df.to_csv(processed_csv, index=False)
        notes.append("Saved full CSV because SAVE_FULL_CSV=1.")
    else:
        notes.append("Full CSV skipped by default for speed. Set SAVE_FULL_CSV=1 if needed.")

    if SAVE_PARQUET:
        try:
            df.to_parquet(OUTPUT_DIR / "processed_airglobal_features.parquet", index=False)
            notes.append("Saved parquet successfully.")
        except Exception as exc:
            notes.append(f"Parquet export skipped: {type(exc).__name__}.")
            log("  ⚠️  Không save được parquet vì thiếu pyarrow/fastparquet. Pickle output đã đủ cho PH-05.")

    summary = PreprocessSummary(
        raw_rows_loaded=int(raw_rows),
        rows_after_cleaning=int(len(df)),
        duplicate_rows_removed=int(duplicate_removed),
        countries=int(df["country"].nunique()) if "country" in df.columns else 0,
        cities=int(df["city"].nunique()) if "city" in df.columns else 0,
        date_from=date_from,
        date_to=date_to,
        numeric_features=int(len(numeric_features)),
        categorical_features=int(len(categorical_features)),
        total_features=int(len(numeric_features) + len(categorical_features)),
        target_col=TARGET_COL,
        label_distribution={str(k): int(v) for k, v in label_dist.to_dict().items()},
        split_distribution={str(k): int(v) for k, v in split_summary.to_dict().items()},
        notes=notes,
    )
    with open(OUTPUT_DIR / "preprocessing_metadata.json", "w", encoding="utf-8") as f:
        json.dump(asdict(summary), f, indent=2, ensure_ascii=False)

    log(f"  ✅ Saved: {processed_pkl.relative_to(BASE_DIR)}")
    log("  ✅ Saved reports: missing_report_before_imputation.csv, outlier_iqr_report.csv, feature_catalog.csv")
    print("\n" + "=" * 80)
    print("✅ PH-03 DONE")
    print(f"Output folder: {OUTPUT_DIR.relative_to(BASE_DIR)}")
    print("Next: python ph05_classification/scripts/train_airglobal_classification.py")
    print("=" * 80)


if __name__ == "__main__":
    main()
