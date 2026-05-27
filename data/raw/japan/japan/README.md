# Japan Air Quality Index (AQI) Dataset — All 47 Prefectures (2014–2025)

**Format:** CSV (UTF-8)  
**Records:** 22,752  
**License:** CC BY-SA 4.0  

---

## About This Dataset

A comprehensive, research-backed Air Quality dataset covering **all 47 Japanese prefectures** with **158 monitoring cities** across a **12-year span (Jan 2014 – Dec 2025)**. Japan maintains one of the densest air quality monitoring networks in the world, and this dataset reflects the country's characteristically low pollution levels, seasonal patterns such as Asian dust (Kosa), and steady improvements under environmental policy.

### Data Sources and Methodology

The dataset is modeled on published data and patterns from the following authentic Japanese government and research platforms:

| Source | Link | Usage |
|---|---|---|
| **MOE** — Ministry of the Environment, Japan | [env.go.jp/en/air/aq](https://www.env.go.jp/en/air/aq/aq.html) | National ambient air quality standards and annual reports |
| **NIES** — National Institute for Environmental Studies | [nies.go.jp/igreen](https://www.nies.go.jp/igreen/) | Historical monitoring station data (PM2.5, PM10, NO2, SO2, CO, O3) |
| **NIES Environmental Data Download** | [tenbou.nies.go.jp/download](https://tenbou.nies.go.jp/download/) | Downloadable CSV archives of air pollution datasets |
| **JMA** — Japan Meteorological Agency | [jma.go.jp](https://www.jma.go.jp/jma/en/Activities/aqi.html) | Wind speed, humidity, and Asian dust (Kosa) advisories |
| **e-Stat** — Portal Site of Official Statistics | [e-stat.go.jp](https://www.e-stat.go.jp/en) | Prefecture-level population density, industrial output |
| **GIO / CGER** — Greenhouse Gas Inventory Office | [nies.go.jp/gio](https://www.nies.go.jp/gio/en/index.html) | Prefecture-level CO2 emission inventories |
| **Forestry Agency, MAFF** | [rinya.maff.go.jp](https://www.rinya.maff.go.jp/) | Forest cover and deforestation statistics |
| **OpenAQ** | [openaq.org](https://openaq.org/) | Open global air quality data aggregation |

### Key Features

- **Complete geographic coverage** — All 47 prefectures (Hokkaido to Okinawa)
- **Monthly granularity** — 144 months (Jan 2014 – Dec 2025)
- **23 columns** — Pollutants, meteorological, socio-economic, and environmental
- **Asian Dust (Kosa) modeling** — Spring PM10 spikes for western Japan prefectures
- **Photochemical Ozone** — Summer O3 peaks reflecting UV-driven photochemistry
- **COVID-19 State of Emergency** — Pollution reduction during Mar–Jun 2020
- **Declining population trend** — Japan's unique demographic shift reflected in density data
- **Gradual CO2 reduction** — Post-Fukushima energy transition modeled

---

## Dataset Specifications

| Property | Value |
|---|---|
| **File** | `japan_air_quality_2014_2025.csv` |
| **Format** | CSV (UTF-8) |
| **Size** | ~2.9 MB |
| **Records** | 22,752 |
| **Prefectures** | 47 |
| **Cities** | 158 |
| **Date Range** | 2014-01-01 to 2025-12-01 |
| **Frequency** | Monthly |

---

## Column Dictionary

### Identifiers

| # | Column | Description | Type |
|---|---|---|---|
| 1 | `Prefecture` | Japanese prefecture name | String |
| 2 | `City` | City or ward name | String |
| 3 | `Date` | Observation date (1st of each month) | Date (YYYY-MM-DD) |

### Air Pollutants

| # | Column | Description | Unit | Type |
|---|---|---|---|---|
| 4 | `PM2.5 (ug/m3)` | Fine Particulate Matter <= 2.5 micrometers | ug/m3 | Float |
| 5 | `PM10 (ug/m3)` | Particulate Matter <= 10 micrometers (SPM equivalent) | ug/m3 | Float |
| 6 | `NO (ug/m3)` | Nitric Oxide | ug/m3 | Float |
| 7 | `NO2 (ug/m3)` | Nitrogen Dioxide | ug/m3 | Float |
| 8 | `NOx (ppb)` | Total Nitrogen Oxides | ppb | Float |
| 9 | `NH3 (ug/m3)` | Ammonia | ug/m3 | Float |
| 10 | `CO (mg/m3)` | Carbon Monoxide | mg/m3 | Float |
| 11 | `SO2 (ug/m3)` | Sulphur Dioxide | ug/m3 | Float |
| 12 | `O3 (ug/m3)` | Ground-level Ozone | ug/m3 | Float |
| 13 | `Benzene (ug/m3)` | Benzene (VOC) | ug/m3 | Float |
| 14 | `Toluene (ug/m3)` | Toluene (VOC) | ug/m3 | Float |
| 15 | `Xylene (ug/m3)` | Xylene (VOC) | ug/m3 | Float |

### Air Quality Index

| # | Column | Description | Type |
|---|---|---|---|
| 16 | `AQI` | Air Quality Index (mapped from PM2.5 using Japan environmental standards) | Integer |
| 17 | `AQI_Bucket` | Category: Good / Moderate / Unhealthy for Sensitive Groups / Unhealthy / Hazardous | String |

### Meteorological Parameters

| # | Column | Description | Unit | Type |
|---|---|---|---|---|
| 18 | `Wind_Speed (km/h)` | Average wind speed | km/h | Float |
| 19 | `Humidity (%)` | Relative humidity | % | Float |

### Socio-Environmental Indicators

| # | Column | Description | Unit | Type |
|---|---|---|---|---|
| 20 | `Deforestation_Rate_%` | Annual deforestation rate | % | Float |
| 21 | `Industry_Growth_%` | Industrial output year-over-year growth | % | Float |
| 22 | `CO2_Emission_MT` | Prefecture-level CO2 emissions | Million Metric Tons | Float |
| 23 | `Population_Density_per_SqKm` | People per square kilometer | per km2 | Float |

---

## Geographic Coverage

### Regions and Prefectures (47)

| Region | Prefectures |
|---|---|
| **Hokkaido** | Hokkaido |
| **Tohoku** | Aomori, Iwate, Miyagi, Akita, Yamagata, Fukushima |
| **Kanto** | Ibaraki, Tochigi, Gunma, Saitama, Chiba, Tokyo, Kanagawa |
| **Chubu** | Niigata, Toyama, Ishikawa, Fukui, Yamanashi, Nagano, Gifu, Shizuoka, Aichi |
| **Kansai** | Mie, Shiga, Kyoto, Osaka, Hyogo, Nara, Wakayama |
| **Chugoku** | Tottori, Shimane, Okayama, Hiroshima, Yamaguchi |
| **Shikoku** | Tokushima, Kagawa, Ehime, Kochi |
| **Kyushu and Okinawa** | Fukuoka, Saga, Nagasaki, Kumamoto, Oita, Miyazaki, Kagoshima, Okinawa |

---

## Pollution Tier Classification

Based on MOE annual air quality reports and NIES monitoring data:

| Tier | Prefectures | PM2.5 Baseline (ug/m3) |
|---|---|---|
| **Urban High** | Tokyo, Osaka, Aichi, Kanagawa, Saitama, Chiba, Fukuoka | 12–35 |
| **Industrial** | Mie, Okayama, Hiroshima, Hyogo, Shizuoka, Ibaraki, Gunma, Tochigi, Gifu, Kyoto, Fukushima | 10–28 |
| **Moderate** | Miyagi, Niigata, Nagano, Toyama, Ishikawa, Nara, Shiga, Yamaguchi, Ehime, Kagawa, Kumamoto, Oita, Nagasaki, Saga, Kagoshima, Wakayama, Fukui | 8–22 |
| **Clean** | Hokkaido, Aomori, Iwate, Akita, Yamagata, Yamanashi, Tottori, Shimane, Tokushima, Kochi, Miyazaki, Okinawa | 4–15 |

---

## Seasonal and Temporal Patterns Modeled

| Season | Months | Effect | Explanation |
|---|---|---|---|
| **Winter** | Dec – Feb | Peak | Temperature inversions trap pollutants; increased heating demand |
| **Spring** | Mar – May | Elevated PM10 | Asian dust (Kosa/Yellow Sand) transported from mainland China and Mongolia affects western prefectures |
| **Summer** | Jun – Aug | Low PM, High O3 | Rain washes out particulates; but photochemical ozone rises due to strong UV |
| **Autumn** | Sep – Nov | Transition | Gradual buildup as temperatures cool |

### Special Events
- **COVID-19 State of Emergency (2020)**: 35–55% pollution reduction during Mar–Jun 2020
- **Post-Fukushima energy shift**: Gradual CO2 reduction as renewable energy adoption increases
- **Asian Dust (Kosa)**: PM10 spikes of up to 40% in western Japan during March and April

---

## Suggested Use Cases

1. **Transboundary Pollution Study** — Analyze the impact of Asian dust on western vs eastern Japan
2. **Photochemical Oxidant Analysis** — Study the summer O3 peaks driven by UV and VOCs
3. **COVID-19 Impact Study** — Quantify changes during the State of Emergency
4. **Demographic Correlation** — Unique opportunity to study declining population vs pollution
5. **Cross-Country Comparison** — Compare with India and China datasets in the `world_AQI` collection
6. **Time Series Forecasting** — ARIMA/LSTM models for AQI prediction
7. **Policy Effectiveness** — Evaluate Japan's environmental regulations over a decade

---

## AQI Reference

| AQI Range | Category | Health Advisory |
|---|---|---|
| 0 – 50 | Good | Air quality is satisfactory |
| 51 – 100 | Moderate | Acceptable; moderate health concern for sensitive individuals |
| 101 – 150 | Unhealthy for Sensitive Groups | Members of sensitive groups may experience health effects |
| 151 – 300 | Unhealthy | Everyone may begin to experience health effects |
| 301 – 500 | Hazardous | Health warnings of emergency conditions |

---

## License and Citation

Released under **[Creative Commons CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**.
You are free to share and adapt this dataset for any purpose, provided you give appropriate credit and distribute contributions under the same license.

Please cite:

```
Japan Air Quality Index Dataset (2014-2025)
All 47 Prefectures | 158 Cities | Monthly Observations (Jan 2014 – Dec 2025)
Data modeled on published statistics from MOE, NIES, JMA, e-Stat, GIO/CGER,
Forestry Agency (MAFF), and OpenAQ.
```
