"""
PH-03: Data Preprocessing & Feature Engineering
Urban Air Quality Intelligence Platform

Nhiệm vụ của An:
- Xử lý missing values: phân tích pattern, interpolation cho gap < 3h, KNN cho gap dài hơn.
- Phát hiện outlier: IQR 1.5x theo trạm/tháng, phân biệt sensor error và ngày ô nhiễm thật.
- Feature engineering: lag, rolling, cyclical/time, spatial/rush-hour/dry-season.
- Tạo target classification cho dự báo AQI label sau 1 giờ.
- Chia train/val/test tránh data leakage và lưu metadata để phase PH-05 dùng lại.

Chạy:
    python ph03_preprocessing/scripts/preprocess_features.py
"""

from __future__ import annotations

import json
import math
import warnings
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).resolve().parents[2]
DATALAKE_AQI = BASE_DIR / "data" / "datalake" / "aqi"
DATALAKE_WEATHER = BASE_DIR / "data" / "datalake" / "weather"
RAW_AQI_DIR = BASE_DIR / "data" / "raw" / "aqi"
RAW_WEATHER_DIR = BASE_DIR / "data" / "raw" / "weather"
STATIONS_CSV = BASE_DIR / "config" / "stations.csv"
OUTPUT_DIR = BASE_DIR / "ph03_preprocessing" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
LAG_HOURS = [1, 3, 6, 12, 24]
ROLLING_WINDOWS = [3, 6, 24]
POLLUTANT_COLS = ["pm25", "pm10", "no2", "o3", "so2", "co", "pm1", "um003"]
WEATHER_RENAME_MAP = {
    "temperature": "temp",
    "temperature_2m": "temp",
    "relative_humidity_2m": "humidity",
    "windspeed": "wind_speed",
    "wind_speed_10m": "wind_speed",
}

# PM2.5 concentration breakpoints, converted to 5 project labels.
# Values are based on common AQI category boundaries; project labels merge the sensitive-group band into "Unhealthy".
PM25_LABEL_THRESHOLDS = [12.0, 35.4, 55.4, 150.4]
LABELS = ["Good", "Moderate", "Unhealthy", "Very_Unhealthy", "Hazardous"]
LABEL_VI = {
    "Good": "Tốt",
    "Moderate": "Trung bình",
    "Unhealthy": "Kém",
    "Very_Unhealthy": "Xấu",
    "Hazardous": "Nguy hại",
}

PHYSICAL_LIMITS = {
    "pm25": (0, 1000),
    "pm10": (0, 2000),
    "pm1": (0, 1000),
    "no2": (0, 5000),
    "o3": (0, 5000),
    "so2": (0, 5000),
    "co": (0, 100000),
    "um003": (0, 100000),
    "temp": (-30, 60),
    "humidity": (0, 100),
    "wind_speed": (0, 80),
    "pressure": (800, 1200),
}

# Approximate anchors for spatial features. These are not used as ground truth; they create simple numeric spatial signals.
INDUSTRIAL_ANCHORS = [
    ("HN_ThangLong_IP", 21.1372, 105.7740),
    ("HN_QuangMinh_IP", 21.1730, 105.7580),
    ("HCM_TanThuan_EPZ", 10.7480, 106.7280),
    ("HCM_LinhTrung_EPZ", 10.8730, 106.7760),
    ("HCM_HiepPhuoc_IP", 10.6440, 106.7400),
]
ROAD_ANCHORS = [
    ("HN_NguyenVanCu", 21.0491, 105.8831),
    ("HN_GiaiPhong", 20.9950, 105.8410),
    ("HCM_DienBienPhu", 10.8010, 106.7130),
    ("HCM_NguyenVanLinh", 10.7380, 106.7200),
]


@dataclass
class PreprocessSummary:
    aqi_rows_loaded: int
    weather_rows_loaded: int
    hourly_rows: int
    rows_after_target: int
    n_stations: int
    date_from: str
    date_to: str
    feature_count: int
    target_col: str
    label_distribution: Dict[str, int]
    split_distribution: Dict[str, int]
    notes: List[str]


def _read_parquet_or_empty(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_parquet(str(path))
    except Exception as exc:
        print(f"  ⚠️  Không đọc được Parquet {path}: {exc.__class__.__name__}. Sẽ dùng raw CSV nếu có.")
        return pd.DataFrame()


def _read_csv_glob(paths: Iterable[Path]) -> pd.DataFrame:
    frames: List[pd.DataFrame] = []
    for p in paths:
        try:
            frames.append(pd.read_csv(p))
        except Exception as exc:
            print(f"  ⚠️  Bỏ qua {p.name}: {exc}")
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def load_aqi_data() -> pd.DataFrame:
    print("\n1️⃣  Loading AQI data...")
    df = _read_parquet_or_empty(DATALAKE_AQI)
    if df.empty:
        df = _read_csv_glob(sorted(RAW_AQI_DIR.glob("summary_*.csv")))
    if df.empty:
        raise FileNotFoundError("Không tìm thấy AQI data trong data/datalake/aqi hoặc data/raw/aqi/summary_*.csv")

    df.columns = [c.strip().lower() for c in df.columns]
    required = {"station_id", "timestamp", "parameter", "value"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"AQI data thiếu cột bắt buộc: {sorted(missing)}")

    if "city" not in df.columns and STATIONS_CSV.exists():
        stations = pd.read_csv(STATIONS_CSV)
        df = df.merge(stations[["station_id", "city", "lat", "lon"]], on="station_id", how="left")

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["parameter"] = df["parameter"].astype(str).str.lower().str.replace(".", "", regex=False)
    df = df.dropna(subset=["station_id", "timestamp", "parameter", "value"])
    print(f"  ✅ AQI: {len(df):,} records | {df['station_id'].nunique()} stations")
    return df


def load_weather_data() -> pd.DataFrame:
    print("\n2️⃣  Loading Weather data...")
    df = _read_parquet_or_empty(DATALAKE_WEATHER)
    if df.empty:
        df = _read_csv_glob(sorted(RAW_WEATHER_DIR.glob("weather_summary_*.csv")))
    if df.empty:
        print("  ⚠️  Không có weather data. Script vẫn chạy với pollutant + time features.")
        return pd.DataFrame()

    df.columns = [WEATHER_RENAME_MAP.get(c.strip().lower(), c.strip().lower()) for c in df.columns]
    if "timestamp" not in df.columns or "station_id" not in df.columns:
        print("  ⚠️  Weather data thiếu station_id/timestamp. Bỏ qua weather.")
        return pd.DataFrame()

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    for col in ["temp", "humidity", "wind_speed", "pressure", "feels_like", "clouds", "wind_deg"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    keep = [c for c in ["station_id", "timestamp", "temp", "humidity", "wind_speed", "pressure", "feels_like", "clouds", "wind_deg"] if c in df.columns]
    df = df[keep].dropna(subset=["station_id", "timestamp"])
    df = df.groupby(["station_id", "timestamp"], as_index=False).mean(numeric_only=True)
    print(f"  ✅ Weather: {len(df):,} records | {df['station_id'].nunique()} stations")
    return df


def build_hourly_matrix(aqi_df: pd.DataFrame, weather_df: pd.DataFrame) -> pd.DataFrame:
    print("\n3️⃣  Building hourly station matrix...")
    static_cols = [c for c in ["station_id", "name", "city", "lat", "lon"] if c in aqi_df.columns]
    use_params = [p for p in POLLUTANT_COLS if p in set(aqi_df["parameter"])]
    if "pm25" not in use_params:
        raise ValueError("Không có parameter 'pm25', không thể tạo target AQI label.")

    grouped = (
        aqi_df[aqi_df["parameter"].isin(use_params)]
        .groupby(static_cols + ["timestamp", "parameter"], dropna=False)["value"]
        .mean()
        .reset_index()
    )
    pivot = grouped.pivot_table(index=static_cols + ["timestamp"], columns="parameter", values="value", aggfunc="mean").reset_index()
    pivot.columns.name = None

    hourly_frames: List[pd.DataFrame] = []
    for station_id, g in pivot.groupby("station_id"):
        g = g.sort_values("timestamp").set_index("timestamp")
        # numeric pollution columns are resampled hourly; station metadata are restored with ffill/bfill.
        numeric_cols = [c for c in g.columns if c not in ["station_id", "name", "city", "lat", "lon"]]
        hr = g[numeric_cols].resample("1H").mean()
        for col in ["station_id", "name", "city", "lat", "lon"]:
            if col in g.columns:
                hr[col] = g[col].dropna().iloc[0] if g[col].notna().any() else np.nan
        hourly_frames.append(hr.reset_index())

    hourly = pd.concat(hourly_frames, ignore_index=True)

    if not weather_df.empty:
        hourly = hourly.merge(weather_df, on=["station_id", "timestamp"], how="left")

    hourly["timestamp"] = pd.to_datetime(hourly["timestamp"], utc=True, errors="coerce")
    hourly = hourly.sort_values(["station_id", "timestamp"]).reset_index(drop=True)
    print(f"  ✅ Hourly matrix: {len(hourly):,} rows | {hourly['station_id'].nunique()} stations | {len(hourly.columns)} columns")
    return hourly


def analyze_missing_patterns(df: pd.DataFrame, numeric_cols: List[str]) -> pd.DataFrame:
    rows = []
    for col in numeric_cols:
        miss = df[col].isna()
        miss_rate = float(miss.mean())
        if miss_rate == 0:
            pattern = "No missing"
        else:
            by_station_std = float(df.assign(_miss=miss).groupby("station_id")["_miss"].mean().std()) if "station_id" in df.columns else 0.0
            by_hour_std = float(df.assign(_miss=miss, _hour=df["timestamp"].dt.hour).groupby("_hour")["_miss"].mean().std()) if "timestamp" in df.columns else 0.0
            if by_station_std > 0.10:
                pattern = "MAR/MNAR-like: phụ thuộc trạm đo"
            elif by_hour_std > 0.10:
                pattern = "MAR-like: phụ thuộc giờ trong ngày"
            else:
                pattern = "MCAR-like: phân bố khá ngẫu nhiên"
        rows.append({
            "feature": col,
            "missing_count": int(miss.sum()),
            "missing_rate": round(miss_rate, 4),
            "suggested_pattern": pattern,
        })
    report = pd.DataFrame(rows).sort_values("missing_rate", ascending=False)
    report.to_csv(OUTPUT_DIR / "missing_pattern_report.csv", index=False, encoding="utf-8-sig")
    print("  ✅ Saved: missing_pattern_report.csv")
    return report


def _detect_sensor_errors(series: pd.Series, lower: float, upper: float) -> Tuple[pd.Series, pd.Series]:
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    if pd.isna(iqr) or iqr == 0:
        iqr_outlier = pd.Series(False, index=series.index)
    else:
        iqr_outlier = (series < q1 - 1.5 * iqr) | (series > q3 + 1.5 * iqr)

    impossible = (series < lower) | (series > upper)
    rolling_med = series.rolling(5, min_periods=3, center=True).median()
    deviation = (series - rolling_med).abs()
    mad = deviation.rolling(24, min_periods=6).median().replace(0, np.nan)
    isolated_spike = iqr_outlier & (deviation > 6 * mad.fillna(deviation.median()))
    sensor_error = impossible | isolated_spike
    return iqr_outlier.fillna(False), sensor_error.fillna(False)


def handle_outliers(df: pd.DataFrame, numeric_cols: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    print("\n4️⃣  Detecting outliers by station/month...")
    out = df.copy()
    out["year_month"] = out["timestamp"].dt.to_period("M").astype(str)
    rows = []

    for col in numeric_cols:
        if col not in PHYSICAL_LIMITS:
            continue
        lower, upper = PHYSICAL_LIMITS[col]
        iqr_col = f"{col}_outlier_iqr"
        err_col = f"{col}_sensor_error"
        out[iqr_col] = False
        out[err_col] = False

        for (_, _), idx in out.groupby(["station_id", "year_month"], dropna=False).groups.items():
            s = out.loc[idx, col]
            if s.notna().sum() < 8:
                continue
            iqr_mask, err_mask = _detect_sensor_errors(s, lower, upper)
            out.loc[idx, iqr_col] = iqr_mask.values
            out.loc[idx, err_col] = err_mask.values

        # Sensor errors are treated as missing; real outliers remain as extreme pollution events.
        out.loc[out[err_col], col] = np.nan
        rows.append({
            "feature": col,
            "iqr_outliers": int(out[iqr_col].sum()),
            "sensor_errors_set_nan": int(out[err_col].sum()),
            "kept_as_real_pollution_events": int((out[iqr_col] & ~out[err_col]).sum()),
        })

    report = pd.DataFrame(rows)
    report.to_csv(OUTPUT_DIR / "outlier_report.csv", index=False, encoding="utf-8-sig")
    print("  ✅ Saved: outlier_report.csv")
    return out.drop(columns=["year_month"]), report


def impute_missing_values(df: pd.DataFrame, numeric_cols: List[str]) -> pd.DataFrame:
    print("\n5️⃣  Imputing missing values: interpolation <3h + KNN/group fallback for longer gaps...")
    out = df.sort_values(["station_id", "timestamp"]).copy()

    # Interpolate small hourly gaps per station; limit=2 means up to two consecutive missing hours.
    for col in numeric_cols:
        out[col] = out.groupby("station_id")[col].transform(lambda s: s.interpolate(method="linear", limit=2, limit_direction="both"))

    remaining_before = int(out[numeric_cols].isna().sum().sum())
    method_used = "none"

    if remaining_before > 0:
        imputer_cols = [c for c in numeric_cols if out[c].notna().sum() > 0]
        # Exact KNNImputer is O(n^2) and can be too slow for a full multi-year hourly matrix.
        # Use it for manageable data; otherwise use station/hour/city median fallback and record the decision.
        if imputer_cols and len(out) <= 20000:
            imputer = KNNImputer(n_neighbors=5, weights="distance")
            out[imputer_cols] = imputer.fit_transform(out[imputer_cols])
            method_used = "KNNImputer(n_neighbors=5)"
        else:
            method_used = "grouped median fallback because dataset is too large for exact KNN in normal laptop runtime"
            out["_hour"] = out["timestamp"].dt.hour
            for col in imputer_cols:
                # Prefer station-hour median, then city-hour median, then global median.
                station_hour = out.groupby(["station_id", "_hour"])[col].transform("median")
                out[col] = out[col].fillna(station_hour)
                if "city" in out.columns:
                    city_hour = out.groupby(["city", "_hour"])[col].transform("median")
                    out[col] = out[col].fillna(city_hour)
                out[col] = out[col].fillna(out[col].median())
            out = out.drop(columns=["_hour"])

    # If a whole column is missing (e.g., weather has no timestamp overlap), fill with neutral median/0 fallback.
    for col in numeric_cols:
        if out[col].isna().any():
            fallback = out[col].median()
            if pd.isna(fallback):
                fallback = 0.0
            out[col] = out[col].fillna(fallback)

    remaining_after = int(out[numeric_cols].isna().sum().sum())
    pd.DataFrame([
        {"stage": "after_interpolation_before_long_gap_impute", "remaining_missing_cells": remaining_before, "method": "linear interpolation limit=2"},
        {"stage": "after_long_gap_impute_and_fallback", "remaining_missing_cells": remaining_after, "method": method_used},
    ]).to_csv(OUTPUT_DIR / "imputation_summary.csv", index=False, encoding="utf-8-sig")
    print(f"  ✅ Missing cells: {remaining_before:,} → {remaining_after:,} | method: {method_used}")
    return out


def pm25_to_label(pm25: float) -> Optional[str]:
    if pd.isna(pm25):
        return None
    if pm25 <= PM25_LABEL_THRESHOLDS[0]:
        return "Good"
    if pm25 <= PM25_LABEL_THRESHOLDS[1]:
        return "Moderate"
    if pm25 <= PM25_LABEL_THRESHOLDS[2]:
        return "Unhealthy"
    if pm25 <= PM25_LABEL_THRESHOLDS[3]:
        return "Very_Unhealthy"
    return "Hazardous"


def haversine_km(lat1: pd.Series, lon1: pd.Series, lat2: float, lon2: float) -> pd.Series:
    r = 6371.0
    phi1 = np.radians(lat1.astype(float))
    phi2 = math.radians(lat2)
    dphi = np.radians(lat2 - lat1.astype(float))
    dlambda = np.radians(lon2 - lon1.astype(float))
    a = np.sin(dphi / 2) ** 2 + np.cos(phi1) * math.cos(phi2) * np.sin(dlambda / 2) ** 2
    return 2 * r * np.arctan2(np.sqrt(a), np.sqrt(1 - a))


def add_spatial_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if not {"lat", "lon"}.issubset(out.columns):
        out["dist_to_nearest_industrial_km"] = np.nan
        out["dist_to_nearest_major_road_km"] = np.nan
        return out

    industrial_dists = [haversine_km(out["lat"], out["lon"], lat, lon) for _, lat, lon in INDUSTRIAL_ANCHORS]
    road_dists = [haversine_km(out["lat"], out["lon"], lat, lon) for _, lat, lon in ROAD_ANCHORS]
    out["dist_to_nearest_industrial_km"] = np.vstack([d.values for d in industrial_dists]).min(axis=0)
    out["dist_to_nearest_major_road_km"] = np.vstack([d.values for d in road_dists]).min(axis=0)
    return out


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    print("\n6️⃣  Feature engineering: lag, rolling, cyclical, spatial...")
    out = df.sort_values(["station_id", "timestamp"]).copy()

    # Current AQI label and next-hour forecasting target.
    out["aqi_label_current"] = out["pm25"].apply(pm25_to_label)
    out["pm25_next_1h"] = out.groupby("station_id")["pm25"].shift(-1)
    out["target_aqi_label_next_1h"] = out["pm25_next_1h"].apply(pm25_to_label)

    base_for_lag = [c for c in ["pm25", "pm10", "no2", "o3", "so2", "co", "temp", "humidity", "wind_speed"] if c in out.columns]
    for col in base_for_lag:
        for lag in LAG_HOURS:
            out[f"{col}_lag_{lag}h"] = out.groupby("station_id")[col].shift(lag)

    for col in [c for c in ["pm25", "pm10", "aqi_numeric", "temp", "humidity", "wind_speed"] if c in out.columns]:
        for window in ROLLING_WINDOWS:
            grouped = out.groupby("station_id")[col]
            out[f"{col}_roll_mean_{window}h"] = grouped.transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
            out[f"{col}_roll_std_{window}h"] = grouped.transform(lambda s: s.shift(1).rolling(window, min_periods=2).std())
            out[f"{col}_roll_max_{window}h"] = grouped.transform(lambda s: s.shift(1).rolling(window, min_periods=1).max())
            out[f"{col}_roll_min_{window}h"] = grouped.transform(lambda s: s.shift(1).rolling(window, min_periods=1).min())

    # Number of hours with current AQI above moderate threshold in previous 24h.
    out["rolling_AQI_exceeds_threshold_24h"] = (
        out.assign(_exceed=(out["pm25"] > PM25_LABEL_THRESHOLDS[1]).astype(int))
        .groupby("station_id")["_exceed"]
        .transform(lambda s: s.shift(1).rolling(24, min_periods=1).sum())
    )

    out["hour"] = out["timestamp"].dt.hour
    out["dayofweek"] = out["timestamp"].dt.dayofweek
    out["month"] = out["timestamp"].dt.month
    out["hour_sin"] = np.sin(2 * np.pi * out["hour"] / 24)
    out["hour_cos"] = np.cos(2 * np.pi * out["hour"] / 24)
    out["dow_sin"] = np.sin(2 * np.pi * out["dayofweek"] / 7)
    out["dow_cos"] = np.cos(2 * np.pi * out["dayofweek"] / 7)
    out["month_sin"] = np.sin(2 * np.pi * out["month"] / 12)
    out["month_cos"] = np.cos(2 * np.pi * out["month"] / 12)
    out["is_rush_hour"] = out["hour"].isin([7, 8, 9, 16, 17, 18, 19]).astype(int)
    out["is_weekend"] = out["dayofweek"].isin([5, 6]).astype(int)
    out["is_dry_season"] = out["month"].isin([11, 12, 1, 2, 3, 4]).astype(int)

    out = add_spatial_features(out)

    # Fill NaNs created by lags/rolling within each station, then global fallback.
    engineered_numeric = out.select_dtypes(include=[np.number]).columns.tolist()
    for col in engineered_numeric:
        out[col] = out.groupby("station_id")[col].transform(lambda s: s.ffill().bfill())
        if out[col].isna().any():
            out[col] = out[col].fillna(out[col].median() if not pd.isna(out[col].median()) else 0.0)

    print(f"  ✅ Feature columns now: {len(out.columns)}")
    return out


def add_split_column(df: pd.DataFrame) -> pd.DataFrame:
    print("\n7️⃣  Splitting train/validation/test without leakage...")
    out = df.dropna(subset=["target_aqi_label_next_1h"]).sort_values("timestamp").copy()
    out["split"] = "train"

    # Temporal holdout: last 15% timestamps are test set.
    unique_times = np.array(sorted(out["timestamp"].dropna().unique()))
    cutoff_index = max(1, int(len(unique_times) * 0.85))
    test_start = unique_times[cutoff_index]
    test_mask = out["timestamp"] >= test_start
    out.loc[test_mask, "split"] = "test"

    train_val_idx = out.index[~test_mask]
    train_val = out.loc[train_val_idx]
    val_size = 0.15 / 0.85
    try:
        train_idx, val_idx = train_test_split(
            train_val.index,
            test_size=val_size,
            stratify=train_val["target_aqi_label_next_1h"],
            random_state=RANDOM_STATE,
        )
    except ValueError:
        train_idx, val_idx = train_test_split(train_val.index, test_size=val_size, random_state=RANDOM_STATE)
    out.loc[val_idx, "split"] = "val"
    out.loc[train_idx, "split"] = "train"

    split_summary = out["split"].value_counts().rename_axis("split").reset_index(name="rows")
    split_summary.to_csv(OUTPUT_DIR / "split_summary.csv", index=False, encoding="utf-8-sig")
    print("  ✅ Split:", split_summary.to_dict("records"))
    return out


def save_feature_catalog(df: pd.DataFrame) -> List[str]:
    non_features = {
        "timestamp", "station_id", "name", "city", "unit", "aqi_label_current", "target_aqi_label_next_1h",
        "pm25_next_1h", "split",
    }
    # Keep numeric features only for sklearn models. Exclude outlier flags only if they are non-numeric; boolean is acceptable.
    feature_cols = [c for c in df.select_dtypes(include=[np.number, bool]).columns if c not in non_features]
    catalog = pd.DataFrame({
        "feature": feature_cols,
        "dtype": [str(df[c].dtype) for c in feature_cols],
        "missing_rate": [round(float(df[c].isna().mean()), 4) for c in feature_cols],
    })
    catalog.to_csv(OUTPUT_DIR / "feature_catalog.csv", index=False, encoding="utf-8-sig")
    print(f"  ✅ Saved feature_catalog.csv ({len(feature_cols)} features)")
    return feature_cols


def write_outputs(df: pd.DataFrame, feature_cols: List[str], summary: PreprocessSummary) -> None:
    csv_path = OUTPUT_DIR / "processed_aqi_features.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"  ✅ Saved: {csv_path.relative_to(BASE_DIR)}")

    try:
        parquet_path = OUTPUT_DIR / "processed_aqi_features.parquet"
        df.to_parquet(parquet_path, index=False)
        print(f"  ✅ Saved: {parquet_path.relative_to(BASE_DIR)}")
    except Exception:
        print("  ⚠️  Không save được Parquet vì thiếu pyarrow/fastparquet. CSV đã đủ cho PH-05.")

    metadata = asdict(summary)
    metadata["feature_columns"] = feature_cols
    metadata["label_mapping_vi"] = LABEL_VI
    metadata["pm25_label_thresholds"] = PM25_LABEL_THRESHOLDS
    metadata["split_strategy"] = "Temporal test holdout last 15% timestamps; stratified train/val on remaining 85%."
    with open(OUTPUT_DIR / "preprocessing_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2, default=str)
    print("  ✅ Saved: preprocessing_metadata.json")


def main() -> None:
    print("=" * 80)
    print("PH-03 PREPROCESSING — AN")
    print("=" * 80)

    notes: List[str] = []
    aqi_df = load_aqi_data()
    weather_df = load_weather_data()
    if not weather_df.empty:
        overlap = (
            max(aqi_df["timestamp"].min(), weather_df["timestamp"].min()),
            min(aqi_df["timestamp"].max(), weather_df["timestamp"].max()),
        )
        if overlap[0] > overlap[1]:
            notes.append("Weather timestamp không overlap với AQI; weather features được impute bằng fallback. Nên crawl lại weather cùng date range để tăng chất lượng mô hình.")
            print("  ⚠️  Weather không overlap với AQI; vẫn giữ columns và impute fallback.")

    hourly = build_hourly_matrix(aqi_df, weather_df)
    numeric_cols = [c for c in hourly.select_dtypes(include=[np.number]).columns if c not in ["lat", "lon"]]
    analyze_missing_patterns(hourly, numeric_cols)
    outlier_handled, _ = handle_outliers(hourly, numeric_cols)
    imputed = impute_missing_values(outlier_handled, numeric_cols)
    featured = feature_engineering(imputed)
    final_df = add_split_column(featured)
    feature_cols = save_feature_catalog(final_df)

    label_distribution = final_df["target_aqi_label_next_1h"].value_counts().to_dict()
    split_distribution = final_df["split"].value_counts().to_dict()
    summary = PreprocessSummary(
        aqi_rows_loaded=int(len(aqi_df)),
        weather_rows_loaded=int(len(weather_df)),
        hourly_rows=int(len(hourly)),
        rows_after_target=int(len(final_df)),
        n_stations=int(final_df["station_id"].nunique()),
        date_from=str(final_df["timestamp"].min()),
        date_to=str(final_df["timestamp"].max()),
        feature_count=int(len(feature_cols)),
        target_col="target_aqi_label_next_1h",
        label_distribution={str(k): int(v) for k, v in label_distribution.items()},
        split_distribution={str(k): int(v) for k, v in split_distribution.items()},
        notes=notes,
    )
    write_outputs(final_df, feature_cols, summary)

    print("\n" + "=" * 80)
    print("✅ PH-03 DONE")
    print("Output folder:", OUTPUT_DIR.relative_to(BASE_DIR))
    print("Next: python ph05_classification/scripts/train_classification.py")
    print("=" * 80)


if __name__ == "__main__":
    main()
