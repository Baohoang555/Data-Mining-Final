"""
EDA Analysis - Urban Air Quality Intelligence Platform
Đọc dữ liệu từ Datalake (Parquet), không dùng locations.json cũ
"""

import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import folium
from folium.plugins import HeatMap
from pathlib import Path
from scipy import stats
from scipy.signal import detrend
from scipy.fft import fft
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.stattools import adfuller
import pyarrow.parquet as pq

warnings.filterwarnings("ignore")

BASE_DIR         = Path(__file__).parent.parent.parent
DATALAKE_AQI     = BASE_DIR / "data" / "datalake" / "aqi"
DATALAKE_WEATHER = BASE_DIR / "data" / "datalake" / "weather"
STATIONS_CSV     = BASE_DIR / "config" / "stations.csv"
OUTPUT_DIR       = BASE_DIR / "ph02_eda" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("EDA ANALYSIS - Urban Air Quality Intelligence Platform")
print("=" * 70)

# ============================================================================
# 1. LOAD DATA từ Datalake
# ============================================================================
print("\n1️⃣  Loading data from Datalake...")

aqi_df = pd.read_parquet(str(DATALAKE_AQI))
aqi_df["timestamp"] = pd.to_datetime(aqi_df["timestamp"], utc=True, errors="coerce")
aqi_df = aqi_df.dropna(subset=["timestamp", "value"])
print(f"  ✅ AQI     : {len(aqi_df):,} records | {aqi_df['station_id'].nunique()} stations")
print(f"              {aqi_df['timestamp'].min()} → {aqi_df['timestamp'].max()}")

weather_df = pd.read_parquet(str(DATALAKE_WEATHER))
weather_df["timestamp"] = pd.to_datetime(weather_df["timestamp"], utc=True, errors="coerce")
weather_df = weather_df.dropna(subset=["timestamp"])
print(f"  ✅ Weather : {len(weather_df):,} records | {weather_df['station_id'].nunique()} stations")

stations_df = pd.read_csv(STATIONS_CSV)
print(f"  ✅ Stations: {len(stations_df)} từ config/stations.csv")

# Station-level summary
locations_df = (
    aqi_df.groupby(["station_id", "name", "city", "lat", "lon"])
    .agg(
        parameter_count=("parameter", "nunique"),
        record_count=("value", "count"),
        date_from=("timestamp", "min"),
        date_to=("timestamp", "max"),
    )
    .reset_index()
)

# ============================================================================
# 2. THỐNG KÊ MÔ TẢ
# ============================================================================
print("\n2️⃣  Descriptive Statistics...")

# PM2.5 focus
pm25 = aqi_df[aqi_df["parameter"] == "pm25"]["value"]

print(f"\n  📊 PM2.5 Statistics:")
print(f"     count  : {pm25.count():,}")
print(f"     mean   : {pm25.mean():.2f} µg/m³")
print(f"     std    : {pm25.std():.2f}")
print(f"     min    : {pm25.min():.2f}")
print(f"     25%    : {pm25.quantile(0.25):.2f}")
print(f"     median : {pm25.median():.2f}")
print(f"     75%    : {pm25.quantile(0.75):.2f}")
print(f"     max    : {pm25.max():.2f}")

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("AQI Descriptive Statistics", fontsize=14, fontweight="bold")

# Histogram PM2.5
axes[0].hist(pm25.clip(upper=pm25.quantile(0.99)), bins=50,
             color="steelblue", edgecolor="white", alpha=0.85)
axes[0].set_xlabel("PM2.5 (µg/m³)")
axes[0].set_ylabel("Count")
axes[0].set_title("PM2.5 Distribution")
axes[0].axvline(pm25.mean(), color="red", linestyle="--", label=f"Mean={pm25.mean():.1f}")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Boxplot by city
city_data = [
    aqi_df[(aqi_df["parameter"] == "pm25") & (aqi_df["city"] == c)]["value"].dropna()
    for c in aqi_df["city"].unique()
]
axes[1].boxplot(city_data, labels=aqi_df["city"].unique(), vert=True, patch_artist=True)
axes[1].set_ylabel("PM2.5 (µg/m³)")
axes[1].set_title("PM2.5 by City")
axes[1].tick_params(axis="x", rotation=15)
axes[1].grid(True, alpha=0.3)

# Record count by parameter
param_counts = aqi_df["parameter"].value_counts()
axes[2].barh(param_counts.index, param_counts.values, color="teal", alpha=0.8)
axes[2].set_xlabel("Record Count")
axes[2].set_title("Records by Parameter")
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "01_descriptive_stats.png", dpi=150, bbox_inches="tight")
print("  ✅ Saved: 01_descriptive_stats.png")
plt.close()

# ============================================================================
# 3. SPATIAL ANALYSIS - Folium Maps
# ============================================================================
print("\n3️⃣  Spatial Analysis...")

city_coords = {
    "Hà Nội": (21.0285, 105.8535),
    "TP.HCM": (10.7769, 106.7009),
}

for city, (clat, clon) in city_coords.items():
    city_stations = locations_df[locations_df["city"] == city]
    if city_stations.empty:
        continue

    m = folium.Map(location=[clat, clon], zoom_start=11, tiles="OpenStreetMap")

    for _, st in city_stations.iterrows():
        folium.CircleMarker(
            location=[st["lat"], st["lon"]],
            radius=8,
            popup=folium.Popup(
                f"<b>{st['name']}</b><br>"
                f"Station: {st['station_id']}<br>"
                f"Records: {st['record_count']:,}<br>"
                f"Parameters: {st['parameter_count']}",
                max_width=200,
            ),
            color="crimson",
            fill=True,
            fill_color="crimson",
            fill_opacity=0.7,
            weight=2,
        ).add_to(m)

    heat_data = [[r["lat"], r["lon"]] for _, r in city_stations.iterrows()]
    HeatMap(heat_data, radius=20, blur=25, max_zoom=1).add_to(m)

    fname = f"02_map_{city.replace('.', '').replace(' ', '_')}.html"
    m.save(OUTPUT_DIR / fname)
    print(f"  ✅ Saved: {fname}")

# ============================================================================
# 4. CORRELATION ANALYSIS
# ============================================================================
print("\n4️⃣  Correlation Analysis...")

# Pivot: 1 row per (station, timestamp), columns = parameters
pivot = (
    aqi_df.groupby(["station_id", pd.Grouper(key="timestamp", freq="D")])["value"]
    .mean()
    .unstack(level=0)
)

# Correlation của PM2.5 với các parameters khác
param_pivot = (
    aqi_df[aqi_df["parameter"].isin(["pm25", "pm10", "no2", "o3", "so2", "co"])]
    .groupby(["timestamp", "parameter"])["value"]
    .mean()
    .unstack("parameter")
    .dropna(how="all")
)

if len(param_pivot) > 10:
    pearson_corr  = param_pivot.corr(method="pearson")
    spearman_corr = param_pivot.corr(method="spearman")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Correlation Matrices — AQI Parameters", fontsize=13, fontweight="bold")

    sns.heatmap(pearson_corr, annot=True, fmt=".2f", cmap="coolwarm",
                center=0, ax=axes[0], square=True, cbar_kws={"label": "r"})
    axes[0].set_title("Pearson Correlation")

    sns.heatmap(spearman_corr, annot=True, fmt=".2f", cmap="coolwarm",
                center=0, ax=axes[1], square=True, cbar_kws={"label": "ρ"})
    axes[1].set_title("Spearman Correlation")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "03_correlation_matrices.png", dpi=150, bbox_inches="tight")
    print("  ✅ Saved: 03_correlation_matrices.png")
    plt.close()

# ============================================================================
# 5. TIME SERIES ANALYSIS
# ============================================================================
print("\n5️⃣  Time Series Analysis...")

# Daily mean PM2.5 toàn quốc
ts = (
    aqi_df[aqi_df["parameter"] == "pm25"]
    .set_index("timestamp")
    .resample("D")["value"]
    .mean()
    .dropna()
)

if len(ts) >= 60:
    # STL Decomposition
    stl    = STL(ts, seasonal=7, period=365 if len(ts) > 365 else 7)
    result = stl.fit()

    fig, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True)
    fig.suptitle("STL Decomposition — Daily Mean PM2.5", fontsize=13, fontweight="bold")

    axes[0].plot(ts.index, ts.values, color="steelblue", linewidth=0.8)
    axes[0].set_ylabel("Original")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(result.trend.index, result.trend, color="red", linewidth=1.2)
    axes[1].set_ylabel("Trend")
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(result.seasonal.index, result.seasonal, color="green", linewidth=0.8)
    axes[2].set_ylabel("Seasonal")
    axes[2].grid(True, alpha=0.3)

    axes[3].plot(result.resid.index, result.resid, color="orange", linewidth=0.6, alpha=0.8)
    axes[3].set_ylabel("Residual")
    axes[3].set_xlabel("Date")
    axes[3].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "04_time_series_decomposition.png", dpi=150, bbox_inches="tight")
    print("  ✅ Saved: 04_time_series_decomposition.png")
    plt.close()

    # ADF Test
    adf = adfuller(ts.dropna())
    print(f"\n  📈 ADF Test (Stationarity):")
    print(f"     ADF Statistic : {adf[0]:.4f}")
    print(f"     p-value       : {adf[1]:.4f}")
    print(f"     {'✅ Stationary' if adf[1] < 0.05 else '⚠️  Non-stationary'} (p {'<' if adf[1] < 0.05 else '>='} 0.05)")

    # FFT
    fft_vals  = np.abs(fft(detrend(ts.values)))
    fft_freqs = np.fft.fftfreq(len(ts))
    half      = len(fft_freqs) // 2

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.semilogy(fft_freqs[1:half], fft_vals[1:half], color="purple", linewidth=0.8)
    ax.set_xlabel("Frequency (cycles/day)")
    ax.set_ylabel("Magnitude (log scale)")
    ax.set_title("FFT — Frequency Domain Analysis (PM2.5)")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "05_fft_frequency_analysis.png", dpi=150, bbox_inches="tight")
    print("  ✅ Saved: 05_fft_frequency_analysis.png")
    plt.close()
else:
    print(f"  ⚠️  Không đủ data cho STL (cần >= 60 ngày, hiện có {len(ts)})")

# ============================================================================
# 6. MORAN'S I - SPATIAL AUTOCORRELATION
# ============================================================================
print("\n6️⃣  Spatial Autocorrelation (Moran's I)...")

try:
    from libpysal.weights import KNN
    from esda.moran import Moran

    spatial_df = (
        aqi_df[aqi_df["parameter"] == "pm25"]
        .groupby(["station_id", "lat", "lon"])["value"]
        .mean()
        .reset_index()
        .rename(columns={"value": "mean_pm25"})
        .dropna()
    )

    if len(spatial_df) >= 4:
        coords = list(zip(spatial_df["lon"], spatial_df["lat"]))
        w      = KNN.from_array(coords, k=min(4, len(spatial_df) - 1))
        w.transform = "r"

        moran = Moran(spatial_df["mean_pm25"].values, w)

        print(f"\n  📐 Moran's I Results:")
        print(f"     I statistic : {moran.I:.4f}")
        print(f"     Expected I  : {moran.EI:.4f}")
        print(f"     p-value     : {moran.p_sim:.4f}")
        print(f"     z-score     : {moran.z_sim:.4f}")

        if moran.p_sim < 0.05:
            label = "Spatial CLUSTERING" if moran.I > moran.EI else "Spatial DISPERSION"
            print(f"     ✅ {label} (p < 0.05)")
        else:
            print(f"     ⚠️  Random spatial pattern (p >= 0.05)")

        # Moran scatter plot
        fig, ax = plt.subplots(figsize=(7, 6))
        lag = w.sparse.dot(spatial_df["mean_pm25"].values)
        ax.scatter(spatial_df["mean_pm25"], lag, alpha=0.7, color="steelblue", edgecolors="white")
        ax.axhline(lag.mean(), color="gray", linestyle="--", linewidth=0.8)
        ax.axvline(spatial_df["mean_pm25"].mean(), color="gray", linestyle="--", linewidth=0.8)
        ax.set_xlabel("Mean PM2.5")
        ax.set_ylabel("Spatial Lag")
        ax.set_title(f"Moran's I Scatter (I={moran.I:.3f}, p={moran.p_sim:.3f})")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "06_morans_i_scatter.png", dpi=150, bbox_inches="tight")
        print("  ✅ Saved: 06_morans_i_scatter.png")
        plt.close()

except ImportError as e:
    print(f"  ⚠️  Thiếu thư viện: {e} → pip install esda libpysal")

# ============================================================================
# 7. AUTO EDA REPORT (ydata-profiling)
# ============================================================================
print("\n7️⃣  Auto EDA Report (ydata-profiling)...")

try:
    from ydata_profiling import ProfileReport

    sample = aqi_df.sample(min(5000, len(aqi_df)), random_state=42)
    sample["timestamp_str"] = sample["timestamp"].astype(str)
    sample = sample.drop(columns=["timestamp"])

    profile = ProfileReport(
        sample,
        title="Urban AQI — EDA Report",
        explorative=True,
        minimal=False,
    )
    report_path = OUTPUT_DIR / "eda_full_report.html"
    profile.to_file(str(report_path))
    print(f"  ✅ Saved: eda_full_report.html")

except ImportError:
    print("  ⚠️  pip install ydata-profiling")
except Exception as e:
    print(f"  ❌ Lỗi: {e}")

# ============================================================================
# 8. SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("📊 EDA SUMMARY")
print("=" * 70)
print(f"\n✅ Output files → {OUTPUT_DIR}")
print("""
  1. 01_descriptive_stats.png        - Histogram, Boxplot, Parameter counts
  2. 02_map_Hà_Nội.html              - Interactive map Hà Nội
  3. 02_map_TP_HCM.html              - Interactive map TP.HCM
  4. 03_correlation_matrices.png     - Pearson & Spearman
  5. 04_time_series_decomposition.png - STL Decompose (Trend/Seasonal/Residual)
  6. 05_fft_frequency_analysis.png   - FFT Analysis
  7. 06_morans_i_scatter.png         - Moran's I Spatial Autocorrelation
  8. eda_full_report.html            - Auto EDA Report (ydata-profiling)
""")
print("=" * 70)