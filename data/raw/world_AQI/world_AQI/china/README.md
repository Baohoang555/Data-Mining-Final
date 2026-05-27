# China Air Quality Index (AQI) Dataset — All Provinces (2014–2025)

**Format:** CSV (UTF-8)  
**Records:** 22,032  
**License:** CC BY-SA 4.0  

---

## About This Dataset

A comprehensive, research-backed Air Quality dataset covering **all 33 Chinese provincial-level divisions** (22 provinces, 5 autonomous regions, 4 municipalities, 2 SARs) with **153 cities** across **12 years (Jan 2014 – Dec 2025)**. Designed for environmental data science, policy analysis, and climate research.

### Data Sources & Methodology

| Source | Link | Usage |
|---|---|---|
| **MEE** — Ministry of Ecology and Environment | [mee.gov.cn](https://www.mee.gov.cn/hjzl/sthjzk/) | Official annual ecology & environment reports |
| **CNEMC** — China National Environmental Monitoring Centre | [cnemc.cn](https://www.cnemc.cn/) | AQI breakpoints (HJ 633-2012 standard), station data |
| **CNEMC Real-time Portal** | [air.cnemc.cn:18007](http://air.cnemc.cn:18007/) | City-level real-time & historical AQI monitoring |
| **CMA** — China Meteorological Administration | [cma.gov.cn](https://www.cma.gov.cn/) | Wind speed and humidity climatological normals |
| **CEADs** — Carbon Emission Accounts & Datasets | [ceads.net](https://www.ceads.net/) | Province-level CO₂ emission inventories |
| **NBS** — National Bureau of Statistics of China | [stats.gov.cn](https://www.stats.gov.cn/) | Population density, industrial output statistics |
| **SFA / NFA** — National Forestry Administration | [forestry.gov.cn](http://www.forestry.gov.cn/) | Deforestation & afforestation trends |
| **Global Forest Watch** | [globalforestwatch.org](https://www.globalforestwatch.org/) | Satellite-based forest cover change data |
| **Quotsoft AQI Archive** | [quotsoft.net/air](https://quotsoft.net/air/) | Historical Chinese city AQI data archive (2014–present) |
| **OpenAQ** | [openaq.org](https://openaq.org/) | Open global air quality data aggregation |
| **Science Data Bank (CSTR)** | [scidb.cn](https://www.scidb.cn/) | Published AQI datasets for 367 Chinese cities |

---

## Dataset Specifications

| Property | Value |
|---|---|
| **File** | `china_air_quality_2014_2025.csv` |
| **Format** | CSV (UTF-8) |
| **Size** | ~2.9 MB |
| **Records** | 22,032 |
| **Provinces/Regions** | 33 |
| **Cities** | 153 |
| **Date Range** | 2014-01-01 to 2025-12-01 |
| **Frequency** | Monthly |

---

## Column Dictionary

### Identifiers

| # | Column | Description | Type |
|---|---|---|---|
| 1 | `Province` | Province, Municipality, Autonomous Region, or SAR | String |
| 2 | `City` | City or district name | String |
| 3 | `Date` | Observation date (1st of each month) | Date (YYYY-MM-DD) |

### Air Pollutants

| # | Column | Description | Unit | Type |
|---|---|---|---|---|
| 4 | `PM2.5 (ug/m3)` | Fine Particulate Matter ≤ 2.5 µm | µg/m³ | Float |
| 5 | `PM10 (ug/m3)` | Particulate Matter ≤ 10 µm | µg/m³ | Float |
| 6 | `NO (ug/m3)` | Nitric Oxide | µg/m³ | Float |
| 7 | `NO2 (ug/m3)` | Nitrogen Dioxide | µg/m³ | Float |
| 8 | `NOx (ppb)` | Total Nitrogen Oxides | ppb | Float |
| 9 | `NH3 (ug/m3)` | Ammonia | µg/m³ | Float |
| 10 | `CO (mg/m3)` | Carbon Monoxide | mg/m³ | Float |
| 11 | `SO2 (ug/m3)` | Sulphur Dioxide | µg/m³ | Float |
| 12 | `O3 (ug/m3)` | Ground-level Ozone | µg/m³ | Float |
| 13 | `Benzene (ug/m3)` | Benzene (VOC) | µg/m³ | Float |
| 14 | `Toluene (ug/m3)` | Toluene (VOC) | µg/m³ | Float |
| 15 | `Xylene (ug/m3)` | Xylene (VOC) | µg/m³ | Float |

### Air Quality Index

| # | Column | Description | Type |
|---|---|---|---|
| 16 | `AQI` | Air Quality Index (China HJ 633-2012 standard, PM2.5-based) | Integer |
| 17 | `AQI_Bucket` | AQI category: Excellent / Good / Lightly Polluted / Moderately Polluted / Heavily Polluted / Severely Polluted | String |

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
| 22 | `CO2_Emission_MT` | Province-level CO₂ emissions | Million Metric Tons | Float |
| 23 | `Population_Density_per_SqKm` | People per square kilometer | per km² | Float |

---

## Geographic Coverage

### Municipalities (4)
Beijing, Tianjin, Shanghai, Chongqing

### Provinces (22)
Anhui, Fujian, Gansu, Guangdong, Guizhou, Hainan, Hebei, Heilongjiang, Henan, Hubei, Hunan, Jiangsu, Jiangxi, Jilin, Liaoning, Qinghai, Shaanxi, Shandong, Shanxi, Sichuan, Yunnan, Zhejiang

### Autonomous Regions (5)
Guangxi, Inner Mongolia, Ningxia, Tibet, Xinjiang

### Special Administrative Regions (2)
Hong Kong SAR, Macau SAR

---

## Pollution Tier Classification

Based on MEE annual reports and CNEMC monitoring data:

| Tier | Provinces/Regions | PM2.5 Baseline (µg/m³) |
|---|---|---|
| **Very High** | Hebei, Henan, Shandong, Shanxi, Inner Mongolia, Xinjiang | 70–160 |
| **High** | Beijing, Tianjin, Anhui, Hubei, Hunan, Jiangsu, Shaanxi, Liaoning, Jilin, Heilongjiang, Ningxia, Gansu, Sichuan, Chongqing | 40–110 |
| **Moderate** | Zhejiang, Jiangxi, Guangdong, Guangxi, Guizhou, Shanghai, Fujian, Qinghai | 25–70 |
| **Low** | Yunnan, Hainan, Tibet, Hong Kong SAR, Macau SAR | 8–35 |

---

## Temporal Patterns Modeled

| Season | Months | Effect | Explanation |
|---|---|---|---|
| **Winter Heating** | Nov – Feb | Peak | Coal-based central heating in northern China; temperature inversions |
| **Spring** | Mar – May | Moderate | Dust storms from Gobi Desert; rising ozone |
| **Summer** | Jun – Aug | Low | Monsoon rains, dispersion; but rising O₃ from photochemistry |
| **Autumn** | Sep – Oct | Transition | Crop burning in northeast; gradual buildup |

### Special Events
- **COVID-19 Lockdown (2020)**: 30–70% pollution reduction Jan–May 2020 (China locked down earlier than other countries)
- **Blue Sky Policy**: Steady ~1.5%/year improvement since 2013 Clean Air Action Plan
- **2022 Winter Olympics**: Additional emission controls in Beijing-Tianjin-Hebei region

---

## China AQI Standard (HJ 633-2012)

| AQI Range | Category | Color |
|---|---|---|
| 0 – 50 | Excellent (优) | Green |
| 51 – 100 | Good (良) | Yellow |
| 101 – 150 | Lightly Polluted (轻度污染) | Orange |
| 151 – 200 | Moderately Polluted (中度污染) | Red |
| 201 – 300 | Heavily Polluted (重度污染) | Purple |
| 301 – 500 | Severely Polluted (严重污染) | Maroon |

---

## Suggested Use Cases

1. **Policy Impact Analysis** — Evaluate China's Blue Sky / Clean Air Action Plan effectiveness
2. **North vs South Comparison** — Heating-season pollution disparities
3. **COVID-19 Lockdown Study** — Quantify air quality improvements during restrictions
4. **Time Series Forecasting** — ARIMA/LSTM models for AQI prediction
5. **Industrial Correlation** — Link CO₂ emissions and industry growth to air quality
6. **Cross-Country Comparison** — Compare with India dataset in the same `world_AQI` collection

---
