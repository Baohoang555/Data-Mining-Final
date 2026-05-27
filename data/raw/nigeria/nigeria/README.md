# Nigeria Air Quality Index (AQI) Dataset (2014–2025)

**Format:** CSV (UTF-8)  
**Records:** 10,368  
**License:** CC BY-SA 4.0  

---

## About This Dataset

A comprehensive, research-backed Air Quality dataset covering **all 36 states and the Federal Capital Territory (FCT) of Nigeria** across **72 major cities** spanning a **12-year period (Jan 2014 – Dec 2025)**. Nigeria faces unique air quality challenges, driven by rapid urbanization, reliance on gasoline generators, industrial activities, and distinct meteorological phenomena. This dataset captures these complex dynamics, offering a realistic model of Nigeria's atmospheric conditions.

### Data Sources and Methodology

Due to the absence of a continuously automated national air quality monitoring network by NESREA, this dataset synthesizes patterns, studies, and satellite-derived estimations from the following verified sources:

| Source | Link | Usage |
|---|---|---|
| **NESREA** | [nesrea.gov.ng](https://www.nesrea.gov.ng/) | National environmental regulations and policy frameworks |
| **AQLI (Univ. of Chicago)** | [aqli.epic.uchicago.edu](https://aqli.epic.uchicago.edu/country/nigeria/) | Long-term particulate pollution exposure modeling for Nigeria |
| **World Bank Data** | [data.worldbank.org](https://data.worldbank.org/indicator/EN.ATM.PM25.MC.M3?locations=NG) | Annual PM2.5 exposure and CO2 emission estimates |
| **NBS** | [nigerianstat.gov.ng](https://nigerianstat.gov.ng/) | National Bureau of Statistics: Population density and industrial growth |
| **Global Forest Watch** | [globalforestwatch.org](https://www.globalforestwatch.org/dashboards/country/NGA/) | Deforestation rates and tree cover loss by state |
| **OpenAQ** | [openaq.org](https://openaq.org/) | Aggregation of independent sensor data in Lagos and Abuja |

### Key Features

- **Geographic coverage** — All 36 Nigerian states plus Abuja (FCT).
- **Monthly granularity** — 144 months (Jan 2014 – Dec 2025).
- **23 columns** — Pollutants, meteorological, socio-economic, and environmental indicators.
- **The Harmattan Season** — Accurately models the severe PM10 and PM2.5 spikes from November to March when Saharan dust blows across West Africa, particularly impacting Northern states (e.g., Kano, Sokoto).
- **Niger Delta Soot** — Captures the chronic, year-round elevated levels of particulate matter, SO2, and VOCs in states like Rivers and Bayelsa due to illegal oil refining and gas flaring.
- **Urban Density** — Reflects the intense vehicular emissions ("Tokunbo" cars) and generator usage in megacities like Lagos.

---

## Dataset Specifications

| Property | Value |
|---|---|
| **File** | `nigeria_air_quality_2014_2025.csv` |
| **Format** | CSV (UTF-8) |
| **Size** | ~1.4 MB |
| **Records** | 10,368 |
| **States/FCT** | 37 |
| **Cities** | 72 |
| **Date Range** | 2014-01-01 to 2025-12-01 |
| **Frequency** | Monthly |

---

## Column Dictionary

### Identifiers

| # | Column | Description | Type |
|---|---|---|---|
| 1 | `State` | Nigerian State or FCT | String |
| 2 | `City` | City name | String |
| 3 | `Date` | Observation date (1st of each month) | Date (YYYY-MM-DD) |

### Air Pollutants

| # | Column | Description | Unit | Type |
|---|---|---|---|---|
| 4 | `PM2.5 (ug/m3)` | Fine Particulate Matter <= 2.5 micrometers | ug/m3 | Float |
| 5 | `PM10 (ug/m3)` | Particulate Matter <= 10 micrometers (Harmattan dust) | ug/m3 | Float |
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
| 16 | `AQI` | Air Quality Index (mapped using standard US EPA breakpoints) | Integer |
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

| Tier | States | PM2.5 Baseline (ug/m3) | Primary Driver |
|---|---|---|---|
| **Severe** | Rivers, Lagos, Kano | 40–150 | Soot (Rivers), Traffic/Pop (Lagos), Harmattan/Pop (Kano) |
| **High** | FCT (Abuja), Kaduna, Oyo, Ogun, Delta, Anambra, Abia | 30–90 | Urbanization, Industry, Oil (Delta) |
| **Moderate** | Edo, Enugu, Osun, Kwara, Sokoto, Borno, Katsina, Plateau | 20–60 | Regional dust, moderate urban traffic |
| **Clean/Rural** | Taraba, Ekiti, Ebonyi, Kogi, Niger, etc. | 10–35 | Lower population density, fewer industries |

---

## Seasonal and Temporal Patterns Modeled

| Season | Months | Effect | Explanation |
|---|---|---|---|
| **Harmattan (Dry)** | Nov – Mar | Severe PM10/PM2.5 Spikes | Dry, dusty trade winds blow from the Sahara over West Africa. Natural dust mixes with urban pollution, creating hazardous conditions, especially in Northern states. |
| **Wet Season** | Apr – Oct | Pollution Washout | Heavy seasonal rains significantly reduce airborne particulate matter, though coastal/delta regions remain humid and affected by local emissions. |

### Special Events
- **The Port Harcourt Soot Crisis**: Modeled as a persistent, year-round elevation in PM2.5, SO2, and VOCs in Rivers State due to artisanal oil refining.
- **Urbanization Trend**: A steady increase in baseline pollution (year-over-year) modeling the rapid population explosion and increasing reliance on diesel/petrol generators across the country.

---

## Suggested Use Cases

1. **Harmattan Impact Analysis** — Isolate Nov–March data to study the disparity in air quality between Northern states (Kano, Sokoto) and Southern states during the dry season.
2. **Environmental Justice** — Analyze the localized pollution (high SO2, VOCs, and PM2.5) in the Niger Delta compared to other regions.
3. **Urban vs. Rural Disparities** — Compare megacities like Lagos and Kano against cleaner, rural states like Taraba.
4. **Cross-Country Analysis** — Compare the impact of Saharan dust in Nigeria to the Asian dust (Kosa) modeled in the Japan dataset of the `world_AQI` collection.

---

## AQI Reference

| AQI Range | Category | Health Advisory |
|---|---|---|
| 0 – 50 | Good | Air quality is satisfactory. |
| 51 – 100 | Moderate | Acceptable; moderate health concern for sensitive individuals. |
| 101 – 150 | Unhealthy for Sensitive Groups | Members of sensitive groups may experience health effects. |
| 151 – 200 | Unhealthy | Everyone may begin to experience health effects. |
| 201 – 300 | Very Unhealthy | Health warnings of emergency conditions. |
| 301 – 500+ | Hazardous | Emergency conditions; the entire population is likely to be affected. |

---

## License and Citation

Released under **[Creative Commons CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**.
You are free to share and adapt this dataset for any purpose, provided you give appropriate credit and distribute contributions under the same license.

Please cite:

```
Nigeria Air Quality Index Dataset (2014-2025)
36 States & FCT | 72 Cities | Monthly Observations (Jan 2014 – Dec 2025)
Data modeled on published statistics from NESREA, AQLI, World Bank, NBS, and Global Forest Watch.
```
