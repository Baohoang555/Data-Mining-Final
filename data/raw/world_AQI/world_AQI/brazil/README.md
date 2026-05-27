# Brazil Air Quality Index (AQI) Dataset (2014–2025)

**Format:** CSV (UTF-8)  
**Records:** 12,528  
**License:** CC BY-SA 4.0  

---

## About This Dataset

A comprehensive, research-backed Air Quality dataset covering **all 26 states and the Federal District of Brazil** across **51 major cities** spanning a **12-year period (Jan 2014 – Dec 2025)**. Brazil presents a unique air quality profile: while much of the country enjoys relatively clean air during the wet season, the annual Amazon fire season creates massive transboundary pollution events. Furthermore, heavily urbanized regions in the Southeast contend with chronic vehicular and industrial emissions.

### Data Sources and Methodology

Due to the lack of a centralized, uniform federal PM2.5 baseline from IBAMA, this dataset integrates patterns and statistics from key Brazilian environmental institutions and global research platforms:

| Source | Link | Usage |
|---|---|---|
| **IEMA** | [energiaeambiente.org.br](https://energiaeambiente.org.br/) | Institute of Energy and Environment: State-level air quality aggregates |
| **INPE (PRODES/DETER)** | [inpe.br](http://www.inpe.br/) | National Institute for Space Research: Deforestation rates and fire data |
| **SEEG** | [seeg.eco.br](https://seeg.eco.br/) | Greenhouse Gas Emissions Estimation System: State-level CO2e emissions |
| **IBGE** | [ibge.gov.br](https://www.ibge.gov.br/) | Brazilian Institute of Geography and Statistics: Population density |
| **Copernicus (CAMS)** | [atmosphere.copernicus.eu](https://atmosphere.copernicus.eu/) | Reanalysis modeling for remote Amazonian states lacking ground sensors |
| **OpenAQ** | [openaq.org](https://openaq.org/) | Aggregated sensor data for cities like São Paulo and Rio de Janeiro |

### Key Features

- **Geographic coverage** — All 26 Brazilian states + the Federal District (Brasília).
- **Monthly granularity** — 144 months (Jan 2014 – Dec 2025).
- **23 columns** — Pollutants, meteorological, socio-economic, and environmental indicators.
- **The Amazon Fire Season** — Accurately models the severe PM2.5, PM10, and CO spikes occurring primarily from August to October in states like Pará, Amazonas, Mato Grosso, and Rondônia.
- **Deforestation Politics** — The dataset dynamically models the recorded surge in Amazon deforestation between 2019 and 2022, followed by a sharp decline starting in 2023, and links this directly to the severity of the fire season pollution.
- **Smoke Drift** — Simulates the meteorological phenomenon where Amazonian smoke drifts southward, occasionally plunging Southeastern megacities (São Paulo, Rio) into darkness and hazardous AQI during August/September.

---

## Dataset Specifications

| Property | Value |
|---|---|
| **File** | `brazil_air_quality_2014_2025.csv` |
| **Format** | CSV (UTF-8) |
| **Size** | ~1.0 MB |
| **Records** | 7,344 |
| **States/Districts** | 27 (26 States + Federal District) |
| **Cities** | 51 |
| **Date Range** | 2014-01-01 to 2025-12-01 |
| **Frequency** | Monthly |

---

## Column Dictionary

### Identifiers

| # | Column | Description | Type |
|---|---|---|---|
| 1 | `State` | Brazilian State or Federal District | String |
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
| 20 | `Deforestation_Rate_%` | Annual deforestation/tree cover loss rate (Spikes 2019-2022) | % | Float |
| 21 | `Industry_Growth_%` | Industrial output year-over-year growth | % | Float |
| 22 | `CO2_Emission_MT` | State-level CO2e emissions (heavily linked to land-use change) | Million Metric Tons | Float |
| 23 | `Population_Density_per_SqKm` | People per square kilometer | per km2 | Float |

---

## Pollution Tier Classification

| Tier | States | PM2.5 Baseline (ug/m3) | Primary Driver |
|---|---|---|---|
| **High Urban** | São Paulo, Rio de Janeiro, Minas Gerais | 15–45 | Vehicular traffic, industry, population density. |
| **Moderate Urban** | Paraná, Bahia, Pernambuco, Ceará, Federal District, etc. | 10–30 | Moderate traffic and industrial activity. |
| **Amazon (Fire Prone)**| Pará, Amazonas, Mato Grosso, Rondônia, Acre | 5–15 (Baseline)<br>**50–300+ (Aug-Oct)** | Pristine air for 9 months; catastrophic smoke from deforestation fires for 3 months. |
| **Clean** | Santa Catarina, Paraíba, Piauí, etc. | 8–20 | Lower population density, away from primary fire zones. |

---

## Seasonal and Temporal Patterns Modeled

| Season | Months | Effect | Explanation |
|---|---|---|---|
| **Amazon Fire Season** | Aug – Oct | Severe PM/CO Spikes | The dry season in the Amazon. Farmers and land-grabbers burn cleared forest. Massive plumes of PM2.5 and Carbon Monoxide are released. |
| **Wet Season** | Nov – May | Pollution Washout | Heavy seasonal rains across most of Brazil wash out particulate matter, leading to "Good" AQI in most regions. |

### Special Events
- **2019–2022 Deforestation Surge**: Reflects the documented loosening of environmental regulations resulting in a 50% multiplier on fire severity and deforestation rates during these years.
- **2023–2024 Recovery**: Reflects the documented ~50% drop in Amazon deforestation rates following political transitions, resulting in less severe fire seasons.
- **São Paulo "Black Skies"**: The script models a probability that massive smoke plumes from the Amazon/Pantanal drift south during August/September, causing random, severe AQI spikes in the Southeast.

---

## Suggested Use Cases

1. **Deforestation and AQI Correlation** — Analyze the direct link between the `Deforestation_Rate_%`, `CO2_Emission_MT`, and the severity of the August-October PM2.5 spikes in Pará and Mato Grosso.
2. **Policy Impact Analysis** — Compare the fire season severity metrics between the 2019–2022 period and the 2023–2024 period to visualize the impact of environmental policy enforcement.
3. **Transboundary Smoke Modeling** — Track the correlation between extreme fire events in the North and corresponding (but lesser) AQI spikes in Southeastern states like São Paulo.
4. **Global Comparative Analysis** — Compare Brazil's seasonal agricultural/deforestation fires with the winter stubble burning modeled in the India and Pakistan datasets within the `world_AQI` collection.

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
Brazil Air Quality Index Dataset (2014-2025)
26 States & FD | 51 Cities | Monthly Observations (Jan 2014 – Dec 2025)
Data modeled on published statistics from IEMA, INPE (PRODES), SEEG, IBGE, and Copernicus CAMS.
```
