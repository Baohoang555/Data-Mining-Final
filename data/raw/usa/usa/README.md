# United States Air Quality Index (AQI) Dataset — All 50 States & DC (2014–2025)

**Format:** CSV (UTF-8)  
**Records:** 28,080  
**License:** CC BY-SA 4.0  

---

## About This Dataset

A comprehensive, research-backed Air Quality dataset covering **all 50 U.S. states plus the District of Columbia** with **184 monitoring cities** across a **12-year span (Jan 2014 – Dec 2025)**. The United States has a diverse climate and industrial landscape, resulting in varying air quality patterns. This dataset captures these dynamics, including the impact of Western wildfires, industrial emissions in the Rust Belt and Texas, and the steady improvements driven by the Clean Air Act.

### Data Sources and Methodology

The dataset is modeled on published data and patterns from the following authentic U.S. government and research platforms:

| Source | Link | Usage |
|---|---|---|
| **EPA AirData** | [epa.gov/outdoor-air-quality-data](https://www.epa.gov/outdoor-air-quality-data) | National ambient air quality standards and historical monitoring data |
| **EPA AQI Basics** | [airnow.gov/aqi/aqi-basics](https://www.airnow.gov/aqi/aqi-basics/) | Official U.S. EPA AQI breakpoints and categories |
| **NOAA NCEI** | [ncei.noaa.gov](https://www.ncei.noaa.gov/) | Climate data including wind speed, humidity, and temperature normals |
| **U.S. Census Bureau** | [census.gov](https://www.census.gov/) | State-level population and population density |
| **EIA** | [eia.gov](https://www.eia.gov/) | State-level energy consumption and CO2 emissions |
| **BEA** | [bea.gov](https://www.bea.gov/) | Industrial output (manufacturing GDP) by state |
| **USDA Forest Service** | [fia.fs.fed.us](https://www.fia.fs.fed.us/) | Forest inventory and analysis, deforestation/tree cover trends |
| **OpenAQ** | [openaq.org](https://openaq.org/) | Open global air quality data aggregation |

### Key Features

- **Complete geographic coverage** — All 50 states + Washington D.C.
- **Monthly granularity** — 144 months (Jan 2014 – Dec 2025)
- **23 columns** — Pollutants, meteorological, socio-economic, and environmental
- **Wildfire modeling** — Summer/Fall PM2.5 and PM10 spikes in Western states (California, Oregon, Washington, etc.)
- **Regional humidity differences** — Arid conditions in the Southwest vs. high humidity in the Southeast
- **COVID-19 Impact** — Pollution reduction during the initial lockdowns in Mar–Jun 2020
- **Clean Air Act improvements** — Modeled gradual reduction in base pollutants over the decade

---

## Dataset Specifications

| Property | Value |
|---|---|
| **File** | `usa_air_quality_2014_2025.csv` |
| **Format** | CSV (UTF-8) |
| **Size** | ~3.3 MB |
| **Records** | 28,080 |
| **States/Districts** | 51 (50 States + DC) |
| **Cities** | 184 |
| **Date Range** | 2014-01-01 to 2025-12-01 |
| **Frequency** | Monthly |

---

## Column Dictionary

### Identifiers

| # | Column | Description | Type |
|---|---|---|---|
| 1 | `State` | U.S. State or District name | String |
| 2 | `City` | City name | String |
| 3 | `Date` | Observation date (1st of each month) | Date (YYYY-MM-DD) |

### Air Pollutants

| # | Column | Description | Unit | Type |
|---|---|---|---|---|
| 4 | `PM2.5 (ug/m3)` | Fine Particulate Matter <= 2.5 micrometers | ug/m3 | Float |
| 5 | `PM10 (ug/m3)` | Particulate Matter <= 10 micrometers | ug/m3 | Float |
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
| 16 | `AQI` | Air Quality Index (mapped from PM2.5 using US EPA standards) | Integer |
| 17 | `AQI_Bucket` | Category: Good / Moderate / Unhealthy for Sensitive Groups / Unhealthy / Very Unhealthy / Hazardous | String |

### Meteorological Parameters

| # | Column | Description | Unit | Type |
|---|---|---|---|---|
| 18 | `Wind_Speed (km/h)` | Average wind speed | km/h | Float |
| 19 | `Humidity (%)` | Relative humidity | % | Float |

### Socio-Environmental Indicators

| # | Column | Description | Unit | Type |
|---|---|---|---|---|
| 20 | `Deforestation_Rate_%` | Annual deforestation/tree cover loss rate | % | Float |
| 21 | `Industry_Growth_%` | Industrial output year-over-year growth | % | Float |
| 22 | `CO2_Emission_MT` | State-level CO2 emissions | Million Metric Tons | Float |
| 23 | `Population_Density_per_SqKm` | People per square kilometer | per km2 | Float |

---

## Pollution Tier Classification

Based on EPA data, population density, and industrial presence:

| Tier | States | PM2.5 Baseline (ug/m3) |
|---|---|---|
| **High** | California, Texas, Pennsylvania, Illinois, Ohio, Indiana, New York, New Jersey | 10–30 |
| **Moderate-High** | Michigan, Florida, Georgia, North Carolina, Arizona, Colorado, Utah, Nevada, Washington, Oregon | 8–25 |
| **Moderate** | Virginia, Maryland, Massachusetts, Tennessee, Missouri, Wisconsin, Minnesota, Louisiana, Alabama, Kentucky, South Carolina, Oklahoma, Connecticut, Iowa, Arkansas, Mississippi, Kansas, New Mexico, Idaho, District of Columbia | 6–20 |
| **Low** | Nebraska, West Virginia, Hawaii, New Hampshire, Maine, Rhode Island, Montana, Delaware, South Dakota, North Dakota, Alaska, Vermont, Wyoming | 3–12 |

---

## Seasonal and Temporal Patterns Modeled

| Season | Months | Effect | Explanation |
|---|---|---|---|
| **Winter** | Dec – Feb | Elevated PM2.5 | Winter temperature inversions, particularly in valleys (e.g., Utah, California) trap pollution; increased heating |
| **Spring** | Mar – May | Transition | Variable winds; generally moderate air quality |
| **Summer** | Jun – Aug | High O3, High PM | Photochemical ozone peaks due to heat and sunlight; Wildfire season begins in the West, dramatically spiking PM2.5/PM10 |
| **Autumn** | Sep – Nov | High PM (Early) | Wildfire season continues into early fall in the West |

### Special Events
- **Western Wildfires**: States like California, Oregon, Washington, Nevada, Idaho, and Colorado see significant, randomized spikes in PM2.5 and PM10 during July-September, reflecting the unpredictable but severe impact of wildfire smoke.
- **COVID-19 Lockdowns (2020)**: 15–40% pollution reduction during Mar–Jun 2020 due to reduced traffic and industrial activity.
- **Long-term Trends**: A gradual ~1.5% annual improvement in base pollution levels reflecting the ongoing impact of the Clean Air Act and shift away from coal.

---

## Suggested Use Cases

1. **Wildfire Impact Analysis** — Study the massive spikes in PM2.5 in Western states during summer/fall compared to baseline levels.
2. **Regional Comparisons** — Compare the industrial pollution of the Rust Belt/Texas to the wildfire-driven pollution of the West Coast.
3. **Socio-Economic Correlation** — Analyze how population density and state-level CO2 emissions relate to overall AQI.
4. **Time Series Forecasting** — Use ARIMA/LSTM to predict AQI, particularly challenging in states with volatile wildfire seasons.
5. **Cross-Country Analysis** — Compare the U.S. dataset with India, China, and Japan in the `world_AQI` collection.

---

## AQI Reference (US EPA Standard)

| AQI Range | Category | Health Advisory |
|---|---|---|
| 0 – 50 | Good | Air quality is satisfactory, and air pollution poses little or no risk. |
| 51 – 100 | Moderate | Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution. |
| 101 – 150 | Unhealthy for Sensitive Groups | Members of sensitive groups may experience health effects. The general public is less likely to be affected. |
| 151 – 200 | Unhealthy | Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects. |
| 201 – 300 | Very Unhealthy | Health alert: The risk of health effects is increased for everyone. |
| 301 – 500 | Hazardous | Health warning of emergency conditions: everyone is more likely to be affected. |

---

## License and Citation

Released under **[Creative Commons CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**.
You are free to share and adapt this dataset for any purpose, provided you give appropriate credit and distribute contributions under the same license.

Please cite:

```
United States Air Quality Index Dataset (2014-2025)
All 50 States & DC | 184 Cities | Monthly Observations (Jan 2014 – Dec 2025)
Data modeled on published statistics from EPA, NOAA, Census Bureau, EIA, BEA, and USDA Forest Service.
```
