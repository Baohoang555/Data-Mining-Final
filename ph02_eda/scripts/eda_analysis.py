import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
from scipy.signal import detrend
from scipy.fft import fft
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.stattools import adfuller

warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATALAKE_AQI = BASE_DIR / "data" / "datalake" / "aqi"
OUTPUT_DIR = BASE_DIR / "ph02_eda" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 72)
print("EDA ANALYSIS - World Air Pollution & AQI Dataset")
print("=" * 72)

# ============================================================================
# 1. LOAD DATA FROM DATALAKE
# ============================================================================
print("\n1. Loading AQI datalake...")

parquet_files = list(DATALAKE_AQI.rglob("*.parquet"))
print(f"   Found {len(parquet_files):,} parquet files")

dfs = []
for file in parquet_files:
    try:
        tmp = pd.read_parquet(file)
        dfs.append(tmp)
    except Exception as e:
        print(f"   Skip {file.name}: {e}")

if not dfs:
    raise ValueError("Không đọc được file parquet nào trong datalake AQI.")

aqi_df = pd.concat(dfs, ignore_index=True)

aqi_df["Date"] = pd.to_datetime(aqi_df["Date"], errors="coerce")
aqi_df = aqi_df.dropna(subset=["Date", "City", "Country", "AQI"])

print(f"   Records : {len(aqi_df):,}")
print(f"   Countries: {aqi_df['Country'].nunique():,}")
print(f"   Cities   : {aqi_df['City'].nunique():,}")
print(f"   Date range: {aqi_df['Date'].min().date()} -> {aqi_df['Date'].max().date()}")

# Chuẩn hoá thêm cột year nếu cần
if "year" not in aqi_df.columns:
    aqi_df["year"] = aqi_df["Date"].dt.year

# Numeric columns cho phân tích
metric_cols = [
    "PM2.5 (ug/m3)", "PM10 (ug/m3)", "NO (ug/m3)", "NO2 (ug/m3)",
    "NH3 (ug/m3)", "CO (mg/m3)", "SO2 (ug/m3)", "O3 (ug/m3)",
    "AQI", "Wind_Speed (km/h)", "Humidity (%)"
]
metric_cols = [c for c in metric_cols if c in aqi_df.columns]

# ============================================================================
# 2. DESCRIPTIVE STATISTICS
# ============================================================================
print("\n2. Descriptive statistics...")

pm25 = aqi_df["PM2.5 (ug/m3)"].dropna() if "PM2.5 (ug/m3)" in aqi_df.columns else pd.Series(dtype=float)

aqi_stats = aqi_df["AQI"].describe()
print("\n   AQI summary:")
print(aqi_stats)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle("Descriptive Statistics - Global AQI Dataset", fontsize=14, fontweight="bold")

axes[0].hist(aqi_df["AQI"].dropna().clip(upper=aqi_df["AQI"].quantile(0.99)), bins=50,
             color="steelblue", edgecolor="white", alpha=0.85)
axes[0].set_title("AQI Distribution")
axes[0].set_xlabel("AQI")
axes[0].set_ylabel("Count")
axes[0].grid(True, alpha=0.3)

if not pm25.empty:
    axes[1].hist(pm25.clip(upper=pm25.quantile(0.99)), bins=50,
                 color="seagreen", edgecolor="white", alpha=0.85)
    axes[1].set_title("PM2.5 Distribution")
    axes[1].set_xlabel("PM2.5 (ug/m3)")
    axes[1].set_ylabel("Count")
    axes[1].grid(True, alpha=0.3)
else:
    axes[1].text(0.5, 0.5, "PM2.5 column not found", ha="center", va="center")
    axes[1].set_title("PM2.5 Distribution")

country_counts = aqi_df["Country"].value_counts().head(10).sort_values()
axes[2].barh(country_counts.index, country_counts.values, color="teal", alpha=0.85)
axes[2].set_title("Top 10 Countries by Record Count")
axes[2].set_xlabel("Records")
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "01_descriptive_stats.png", dpi=150, bbox_inches="tight")
print("   Saved: 01_descriptive_stats.png")
plt.close()

# ============================================================================
# 3. TOP CITIES ANALYSIS
# ============================================================================
print("\n3. Top cities analysis...")

city_aqi = (
    aqi_df.groupby(["Country", "City"], as_index=False)
    .agg(
        mean_aqi=("AQI", "mean"),
        median_aqi=("AQI", "median"),
        record_count=("AQI", "count")
    )
    .query("record_count >= 30")
    .sort_values("mean_aqi", ascending=False)
)

print("\n   Top 10 cities by mean AQI (min 30 records):")
print(city_aqi.head(10).to_string(index=False))

top10 = city_aqi.head(10).sort_values("mean_aqi")
fig, ax = plt.subplots(figsize=(12, 6))
labels = top10["City"] + " (" + top10["Country"] + ")"
ax.barh(labels, top10["mean_aqi"], color="crimson", alpha=0.85)
ax.set_title("Top 10 Most Polluted Cities by Mean AQI")
ax.set_xlabel("Mean AQI")
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "02_top_polluted_cities.png", dpi=150, bbox_inches="tight")
print("   Saved: 02_top_polluted_cities.png")
plt.close()

# ============================================================================
# 4. SPATIAL ANALYSIS (COUNTRY-CITY AVAILABILITY)
# ============================================================================
print("\n4. Spatial analysis...")

# Tạo map cho Việt Nam nếu có dữ liệu lat/lon thì không, dataset hiện không có lat/lon
# Thay bằng city concentration theo country
country_city = (
    aqi_df.groupby("Country")["City"]
    .nunique()
    .sort_values(ascending=False)
    .head(15)
)

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(country_city.index, country_city.values, color="darkorange", alpha=0.85)
ax.set_title("Top 15 Countries by Number of Cities")
ax.set_ylabel("Unique Cities")
ax.tick_params(axis="x", rotation=45)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "03_country_city_coverage.png", dpi=150, bbox_inches="tight")
print("   Saved: 03_country_city_coverage.png")
plt.close()

# ============================================================================
# 5. CORRELATION ANALYSIS
# ============================================================================
print("\n5. Correlation analysis...")

corr_df = aqi_df[metric_cols].copy().dropna(how="all")
if len(corr_df) > 10 and len(metric_cols) >= 2:
    pearson_corr = corr_df.corr(method="pearson")
    spearman_corr = corr_df.corr(method="spearman")

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle("Correlation Matrices - Air Quality Variables", fontsize=14, fontweight="bold")

    sns.heatmap(pearson_corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
                ax=axes[0], square=True, cbar_kws={"label": "r"})
    axes[0].set_title("Pearson Correlation")

    sns.heatmap(spearman_corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
                ax=axes[1], square=True, cbar_kws={"label": "ρ"})
    axes[1].set_title("Spearman Correlation")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "04_correlation_matrices.png", dpi=150, bbox_inches="tight")
    print("   Saved: 04_correlation_matrices.png")
    plt.close()
else:
    print("   Not enough numeric data for correlation analysis.")

# ============================================================================
# 6. TIME SERIES ANALYSIS
# ============================================================================
print("\n6. Time series analysis...")

ts = (
    aqi_df.groupby("Date", as_index=True)["AQI"]
    .mean()
    .sort_index()
    .dropna()
)

if len(ts) >= 60:
    stl_period = 365 if len(ts) >= 365 else 7
    stl = STL(ts, period=stl_period, seasonal=7)
    result = stl.fit()

    fig, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True)
    fig.suptitle("STL Decomposition - Daily Mean AQI", fontsize=14, fontweight="bold")

    axes[0].plot(ts.index, ts.values, color="steelblue", linewidth=0.8)
    axes[0].set_ylabel("Original")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(result.trend.index, result.trend, color="red", linewidth=1.0)
    axes[1].set_ylabel("Trend")
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(result.seasonal.index, result.seasonal, color="green", linewidth=0.8)
    axes[2].set_ylabel("Seasonal")
    axes[2].grid(True, alpha=0.3)

    axes[3].plot(result.resid.index, result.resid, color="orange", linewidth=0.7)
    axes[3].set_ylabel("Residual")
    axes[3].set_xlabel("Date")
    axes[3].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "05_time_series_decomposition.png", dpi=150, bbox_inches="tight")
    print("   Saved: 05_time_series_decomposition.png")
    plt.close()

    adf = adfuller(ts.dropna())
    print("\n   ADF Test:")
    print(f"   ADF Statistic: {adf[0]:.4f}")
    print(f"   p-value      : {adf[1]:.4f}")
    print(f"   Result       : {'Stationary' if adf[1] < 0.05 else 'Non-stationary'}")

    fft_vals = np.abs(fft(detrend(ts.values)))
    fft_freqs = np.fft.fftfreq(len(ts))
    half = len(fft_freqs) // 2

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.semilogy(fft_freqs[1:half], fft_vals[1:half], color="purple", linewidth=0.8)
    ax.set_xlabel("Frequency (cycles/day)")
    ax.set_ylabel("Magnitude (log scale)")
    ax.set_title("FFT - Frequency Domain Analysis (AQI)")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "06_fft_frequency_analysis.png", dpi=150, bbox_inches="tight")
    print("   Saved: 06_fft_frequency_analysis.png")
    plt.close()
else:
    print(f"   Not enough time points for STL. Current length: {len(ts)}")

# ============================================================================
# 7. VIETNAM FOCUS
# ============================================================================
print("\n7. Vietnam focus...")

vn_df = aqi_df[aqi_df["Country"].astype(str).str.lower() == "vietnam"].copy()
if not vn_df.empty:
    vn_city = (
        vn_df.groupby("City", as_index=False)
        .agg(mean_aqi=("AQI", "mean"), record_count=("AQI", "count"))
        .sort_values("mean_aqi", ascending=False)
    )

    print("\n   Vietnam cities by mean AQI:")
    print(vn_city.head(10).to_string(index=False))

    top_vn = vn_city.head(10).sort_values("mean_aqi")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(top_vn["City"], top_vn["mean_aqi"], color="forestgreen", alpha=0.85)
    ax.set_title("Top Vietnam Cities by Mean AQI")
    ax.set_xlabel("Mean AQI")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "07_vietnam_top_cities.png", dpi=150, bbox_inches="tight")
    print("   Saved: 07_vietnam_top_cities.png")
    plt.close()
else:
    print("   Vietnam data not found in dataset.")

# ============================================================================
# 8. SUMMARY
# ============================================================================
print("\n" + "=" * 72)
print("EDA SUMMARY")
print("=" * 72)
print(f"Output directory: {OUTPUT_DIR}")
print("Generated files:")
print("  1. 01_descriptive_stats.png")
print("  2. 02_top_polluted_cities.png")
print("  3. 03_country_city_coverage.png")
print("  4. 04_correlation_matrices.png")
print("  5. 05_time_series_decomposition.png")
print("  6. 06_fft_frequency_analysis.png")
print("  7. 07_vietnam_top_cities.png (nếu có dữ liệu Việt Nam)")
print("=" * 72)