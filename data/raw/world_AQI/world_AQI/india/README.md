# India Air Quality Index (AQI) Dataset — All States & UTs (2014–2025)

**Format:** CSV (UTF-8)  
**Records:** 20,592  
**License:** CC BY-SA 4.0  

---

## About This Dataset

A comprehensive, research-backed Air Quality dataset covering **all 36 Indian States and Union Territories** with **142 monitoring cities** across a **12-year span (Jan 2014 – Dec 2025)**. This dataset is ideal for environmental data science, time-series analysis, policy evaluation, and climate research.

### Data Sources & Methodology

The dataset is modeled on published data and patterns from the following **authentic Indian government and research platforms**:

| Source | Link | Usage |
|---|---|---|
| **CPCB** — Central Pollution Control Board | [app.cpcbccr.com/ccr](https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing) | Pollutant baselines — PM2.5, PM10, NO₂, SO₂, CO, NH₃, O₃ |
| **CPCB Data Repository** | [cpcb.nic.in/air-quality-data](https://cpcb.nic.in/air-quality-data/) | Historical AQI bulletins and NAMP station data |
| **IMD** — India Meteorological Department | [mausam.imd.gov.in](https://mausam.imd.gov.in/) | Wind speed and humidity climatological normals |
| **MoEFCC** — Ministry of Environment | [moef.gov.in](https://moef.gov.in/) | Deforestation rates, NCAP policy |
| **NCAP Tracker** | [ncaptracker.in](https://www.ncaptracker.in/) | National Clean Air Programme city-level targets |
| **ISFR** — India State of Forest Report | [fsi.nic.in/forest-report](https://fsi.nic.in/forest-report) | Forest cover change and deforestation trends |
| **MoSPI / Census of India** | [censusindia.gov.in](https://censusindia.gov.in/) | State-wise population density |
| **UrbanEmissions.info** | [urbanemissions.info/india-air-quality](https://urbanemissions.info/india-air-quality/) | AQI trend analysis and monitoring data validation |
| **ASI** — Annual Survey of Industries | [mospi.gov.in/annual-survey-industries](https://mospi.gov.in/annual-survey-industries) | State-wise industrial growth rates |
| **Global Carbon Project** | [globalcarbonproject.org](https://www.globalcarbonproject.org/carbonbudget/) | CO₂ emission baselines per state |
| **data.gov.in** | [data.gov.in](https://data.gov.in/) | Open government datasets under NDSAP |

### Key Features

- **Complete geographic coverage** — All 28 states + 8 union territories
- **Monthly granularity** — 144 months (Jan 2014 – Dec 2025)
- **23 columns** — Pollutants, meteorological, socio-economic, and environmental
- **Seasonal patterns** — Winter peaks, monsoon dips, dust storm effects
- **COVID-19 lockdown impact** — Realistic pollution reduction in Mar–Jun 2020
- **NCAP policy effects** — Post-2020 improvement trends in high-pollution states
- **Tier-based realism** — States classified by pollution severity for accurate baselines

---

## Dataset Specifications

| Property | Value |
|---|---|
| **File** | `india_air_quality_2014_2025.csv` |
| **Format** | CSV (UTF-8) |
| **Size** | ~2.8 MB |
| **Records** | 20,592 |
| **States/UTs** | 36 |
| **Cities** | 142 |
| **Date Range** | 2014-01-01 to 2025-12-01 |
| **Frequency** | Monthly |

---

## Column Dictionary

### Identifiers

| # | Column | Description | Type |
|---|---|---|---|
| 1 | `State` | Indian State or Union Territory name | String |
| 2 | `City` | City / monitoring station location | String |
| 3 | `Date` | Date of observation (1st of each month) | Date (YYYY-MM-DD) |

### Air Pollutants

| # | Column | Description | Unit | Type |
|---|---|---|---|---|
| 4 | `PM2.5 (ug/m3)` | Particulate Matter ≤ 2.5 micrometers | µg/m³ | Float |
| 5 | `PM10 (ug/m3)` | Particulate Matter ≤ 10 micrometers | µg/m³ | Float |
| 6 | `NO (ug/m3)` | Nitric Oxide concentration | µg/m³ | Float |
| 7 | `NO2 (ug/m3)` | Nitrogen Dioxide concentration | µg/m³ | Float |
| 8 | `NOx (ppb)` | Total Nitrogen Oxides | ppb | Float |
| 9 | `NH3 (ug/m3)` | Ammonia concentration | µg/m³ | Float |
| 10 | `CO (mg/m3)` | Carbon Monoxide concentration | mg/m³ | Float |
| 11 | `SO2 (ug/m3)` | Sulphur Dioxide concentration | µg/m³ | Float |
| 12 | `O3 (ug/m3)` | Ground-level Ozone concentration | µg/m³ | Float |
| 13 | `Benzene (ug/m3)` | Benzene (VOC) concentration | µg/m³ | Float |
| 14 | `Toluene (ug/m3)` | Toluene (VOC) concentration | µg/m³ | Float |
| 15 | `Xylene (ug/m3)` | Xylene (VOC) concentration | µg/m³ | Float |

### Air Quality Index

| # | Column | Description | Type |
|---|---|---|---|
| 16 | `AQI` | Air Quality Index (computed from PM2.5 via Indian NAQI breakpoints) | Integer |
| 17 | `AQI_Bucket` | AQI category: Good / Satisfactory / Moderate / Poor / Very Poor / Severe | String |

### Meteorological Parameters

| # | Column | Description | Unit | Type |
|---|---|---|---|---|
| 18 | `Wind_Speed (km/h)` | Average wind speed | km/h | Float |
| 19 | `Humidity (%)` | Relative humidity | % | Float |

### Socio-Environmental Indicators

| # | Column | Description | Unit | Type |
|---|---|---|---|---|
| 20 | `Deforestation_Rate_%` | Annual deforestation rate for the state | % | Float |
| 21 | `Industry_Growth_%` | Year-over-year industrial output growth | % | Float |
| 22 | `CO2_Emission_MT` | State-level CO₂ emissions | Metric Tons (millions) | Float |
| 23 | `Population_Density_per_SqKm` | People per square kilometer | per km² | Float |

---

## Geographic Coverage

### States (28)
Andhra Pradesh, Arunachal Pradesh, Assam, Bihar, Chhattisgarh, Goa, Gujarat, Haryana, Himachal Pradesh, Jharkhand, Karnataka, Kerala, Madhya Pradesh, Maharashtra, Manipur, Meghalaya, Mizoram, Nagaland, Odisha, Punjab, Rajasthan, Sikkim, Tamil Nadu, Telangana, Tripura, Uttar Pradesh, Uttarakhand, West Bengal

### Union Territories (8)
Andaman & Nicobar Islands, Chandigarh, Dadra & Nagar Haveli and Daman & Diu, Delhi (NCT), Jammu & Kashmir, Ladakh, Lakshadweep, Puducherry

---

## Pollution Tier Classification

States are classified into pollution tiers based on published CPCB annual reports and WHO data:

| Tier | States | PM2.5 Baseline (µg/m³) |
|---|---|---|
| **Very High** | Delhi, Uttar Pradesh, Bihar, Haryana, Punjab, Jharkhand, Rajasthan | 80–180 |
| **High** | Chhattisgarh, Madhya Pradesh, West Bengal, Odisha, Maharashtra, Gujarat | 50–130 |
| **Moderate** | Andhra Pradesh, Telangana, Tamil Nadu, Karnataka, Assam, Uttarakhand | 30–80 |
| **Low** | Kerala, Goa, Sikkim, Himachal Pradesh, NE states, island territories | 10–45 |

---

## Seasonal & Temporal Patterns Modeled

| Season | Months | Pollution Effect | Explanation |
|---|---|---|---|
| **Winter** | Nov – Feb | Peak | Temperature inversions trap pollutants; crop stubble burning in Indo-Gangetic plain |
| **Pre-Monsoon** | Mar – May | Moderate | Dust storms in Rajasthan/North; rising ozone from heat |
| **Monsoon** | Jun – Sep | Minimum | Rainfall washes out particulates; strong winds disperse pollutants |
| **Post-Monsoon** | Oct | Transition | Gradual buildup as temperatures drop |

### Special Events
- **COVID-19 Lockdown (2020)**: 50–70% reduction in pollutant levels during Mar–Jun 2020
- **NCAP Policy (post-2020)**: Gradual 2–3% improvement trend in high-pollution states

---

## Suggested Use Cases

1. **Time Series Forecasting** — Predict AQI using ARIMA, Prophet, or LSTM models
2. **Correlation Analysis** — Link CO₂ emissions, industry growth, and deforestation to air quality
3. **State Comparison** — Compare pollution across regions (North vs. South, Urban vs. Rural)
4. **Policy Impact Assessment** — Evaluate NCAP effectiveness using pre/post-2020 data
5. **COVID-19 Impact Study** — Analyze lockdown effects on air quality
6. **Seasonal Pattern Mining** — Identify recurring pollution cycles
7. **Health Impact Modeling** — Correlate AQI with population density
8. **Climate & Weather Interaction** — Study wind speed and humidity effects on pollution dispersion

---

## AQI Breakpoint Reference (India NAQI Standard)

| AQI Range | Category | Health Impact |
|---|---|---|
| 0 – 50 | Good | Minimal impact |
| 51 – 100 | Satisfactory | Minor breathing discomfort for sensitive people |
| 101 – 200 | Moderate | Breathing discomfort for people with lung/heart disease |
| 201 – 300 | Poor | Breathing discomfort on prolonged exposure |
| 301 – 400 | Very Poor | Respiratory illness on prolonged exposure |
| 401 – 500 | Severe | Affects healthy people; serious impact on those with existing diseases |

---
