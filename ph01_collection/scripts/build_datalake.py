import json
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
from tqdm import tqdm

BASE_DIR         = Path(__file__).parent.parent.parent
RAW_AQI_DIR      = BASE_DIR / "data" / "raw" / "aqi"
RAW_WEATHER_DIR  = BASE_DIR / "data" / "raw" / "weather"
DATALAKE_DIR     = BASE_DIR / "data" / "datalake"
STATIONS_CSV     = BASE_DIR / "config" / "stations.csv"
DATALAKE_DIR.mkdir(parents=True, exist_ok=True)

STATIONS = pd.read_csv(STATIONS_CSV)

print("=" * 70)
print("BUILD DATA LAKE - Raw JSON → Parquet (Partitioned)")
print("=" * 70)


def build_aqi_datalake():
    """Merge raw AQI JSON files thành Parquet partitioned (city/year/month)."""
    print("\n🔨 Building AQI Data Lake...")

    if not RAW_AQI_DIR.exists():
        print("⚠️  Thư mục raw AQI không tồn tại, bỏ qua...")
        return

    aqi_records = []
    station_dirs = [d for d in RAW_AQI_DIR.glob("*") if d.is_dir()]

    for station_dir in tqdm(station_dirs, desc="AQI Stations"):
        station_id   = station_dir.name
        station_info = STATIONS[STATIONS["station_id"] == station_id]

        if station_info.empty:
            continue

        station_row = station_info.iloc[0]

        for json_file in station_dir.glob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Support cả 2 format: list trực tiếp hoặc {"results": [...]}
                records_list = data if isinstance(data, list) else data.get("results", [])

                for record in records_list:
                    aqi_records.append({
                        "station_id": record.get("station_id", station_id),
                        "name":       record.get("name", station_row["name"]),
                        "city":       record.get("city", station_row["city"]),
                        "lat":        record.get("lat",  station_row["lat"]),
                        "lon":        record.get("lon",  station_row["lon"]),
                        "timestamp":  record.get("timestamp"),
                        "parameter":  record.get("parameter"),
                        "value":      record.get("value"),
                        "unit":       record.get("unit"),
                    })

            except Exception as e:
                print(f"⚠️  Lỗi parse {json_file.name}: {e}")
                continue

    if aqi_records:
        df = pd.DataFrame(aqi_records)

        # Convert timestamp
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        df = df.dropna(subset=["timestamp"])

        df["year"]  = df["timestamp"].dt.year
        df["month"] = df["timestamp"].dt.month

        # Drop duplicates
        df = df.drop_duplicates(subset=["station_id", "timestamp", "parameter"])

        print(f"\n   📊 Records      : {len(df):,}")
        print(f"   📊 Stations     : {df['station_id'].nunique()}")
        print(f"   📊 Parameters   : {sorted(df['parameter'].dropna().unique())}")
        print(f"   📊 Date range   : {df['timestamp'].min()} → {df['timestamp'].max()}")
        print(f"   📊 Cities       : {df['city'].value_counts().to_dict()}")

        # Write partitioned Parquet
        table = pa.Table.from_pandas(df, preserve_index=False)
        pq.write_to_dataset(
            table,
            root_path=str(DATALAKE_DIR / "aqi"),
            partition_cols=["city", "year", "month"],
            existing_data_behavior="overwrite_or_ignore",
        )
        print(f"\n   ✅ AQI Parquet saved → data/datalake/aqi/")
    else:
        print("⚠️  Không có dữ liệu AQI")


def build_weather_datalake():
    """Merge raw Weather CSV/JSON files thành Parquet partitioned."""
    print("\n🔨 Building Weather Data Lake...")

    if not RAW_WEATHER_DIR.exists():
        print("⚠️  Thư mục raw Weather không tồn tại, bỏ qua...")
        return

    weather_records = []

    # Đọc từ summary CSV (output của crawl_weather.py)
    csv_files = list(RAW_WEATHER_DIR.glob("weather_summary_*.csv"))

    if csv_files:
        for csv_file in tqdm(csv_files, desc="Weather CSVs"):
            try:
                df_raw = pd.read_csv(csv_file)
                weather_records.append(df_raw)
                print(f"   ✅ Loaded {len(df_raw):,} records từ {csv_file.name}")
            except Exception as e:
                print(f"⚠️  Lỗi đọc {csv_file.name}: {e}")

    # Đọc thêm từ JSON nếu có
    for station_dir in RAW_WEATHER_DIR.glob("*"):
        if not station_dir.is_dir():
            continue
        for json_file in station_dir.glob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                records_list = data if isinstance(data, list) else data.get("results", [])
                if records_list:
                    weather_records.append(pd.DataFrame(records_list))
            except Exception as e:
                print(f"⚠️  Lỗi parse {json_file.name}: {e}")

    if weather_records:
        df = pd.concat(weather_records, ignore_index=True)

        # Convert timestamp
        ts_col = "timestamp" if "timestamp" in df.columns else "time"
        df[ts_col] = pd.to_datetime(df[ts_col], utc=True, errors="coerce")
        df = df.dropna(subset=[ts_col])
        if ts_col != "timestamp":
            df = df.rename(columns={ts_col: "timestamp"})

        df["year"]  = df["timestamp"].dt.year
        df["month"] = df["timestamp"].dt.month

        # Drop duplicates
        df = df.drop_duplicates(subset=["station_id", "timestamp"])

        print(f"\n   📊 Records      : {len(df):,}")
        print(f"   📊 Stations     : {df['station_id'].nunique()}")
        print(f"   📊 Date range   : {df['timestamp'].min()} → {df['timestamp'].max()}")
        print(f"   📊 Cities       : {df['city'].value_counts().to_dict()}")

        # Write partitioned Parquet
        table = pa.Table.from_pandas(df, preserve_index=False)
        pq.write_to_dataset(
            table,
            root_path=str(DATALAKE_DIR / "weather"),
            partition_cols=["city", "year", "month"],
            existing_data_behavior="overwrite_or_ignore",
        )
        print(f"\n   ✅ Weather Parquet saved → data/datalake/weather/")
    else:
        print("⚠️  Không có dữ liệu Weather")


if __name__ == "__main__":
    build_aqi_datalake()
    build_weather_datalake()

    print("\n" + "=" * 70)
    print("✅ Data Lake build xong!")
    print(f"📁 Location: {DATALAKE_DIR}")
    print("=" * 70)