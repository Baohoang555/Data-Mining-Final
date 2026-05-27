# Mexico Air Quality Index (AQI) Dataset (2014-2025)

**Format:** CSV (UTF-8)  
**Records:** 12,672  
**License:** CC BY-SA 4.0  

---

## About This Dataset

A comprehensive, research-backed Air Quality dataset covering **all 31 States and Mexico City (CDMX)** with **88 major cities** across a **12-year span (Jan 2014 -- Dec 2025)**. 

Mexico's air quality is heavily influenced by its unique topography and rapid industrialization. This dataset accurately models the chronic high-altitude thermal inversions that trap severe smog in the Valley of Mexico (CDMX, Toluca), the heavy industrial particulate matter of Monterrey and Saltillo, the dense traffic emissions of Guadalajara, and the seasonal biomass burning driven by deforestation in the southern states (Chiapas, Campeche, Oaxaca).

> [!NOTE]
> **Real-World Missing Data Simulation**: Per user specification, this dataset intentionally includes approximately **~4.0% missing values (nulls)** for pollutant columns. This accurately simulates real-world sensor downtime and data gaps common in national monitoring networks. The missing rate is kept strictly under 8%.

### Data Sources and Methodology

This dataset synthesizes pollution patterns, baselines, and seasonal dynamics from the following verified sources:

| Source | Link | Usage |
|---|---|---|
| **SINAICA / INECC** | [sinaica.inecc.gob.mx](https://sinaica.inecc.gob.mx/) | National Air Quality Information System data and local monitoring networks |
| **SEDEMA (CDMX)** | [aire.cdmx.gob.mx](http://www.aire.cdmx.gob.mx/) | Real-time and historical air quality data specifically for the Valley of Mexico |
| **IQAir** | [iqair.com/mexico](https://www.iqair.com/mexico) | Annual PM2.5 baselines and historical city rankings |
| **World Bank** | [data.worldbank.org](https://data.worldbank.org/) | Annual PM2.5 exposure and CO2 emission estimates |
| **INEGI** | [inegi.org.mx](https://www.inegi.org.mx/) | National Institute of Statistics and Geography for population density and industrial growth |
| **Global Forest Watch** | [globalforestwatch.org](https://www.globalforestwatch.org/) | Deforestation rates and tree cover loss primarily in southern Mexico |

### Key Features

- **Geographic coverage** -- All 32 federal entities (31 states + CDMX).
- **Monthly granularity** -- 144 months (Jan 2014 -- Dec 2025).
- **23 columns** -- Pollutants, meteorological, socio-economic, and environmental indicators.
- **High-Altitude Basins** -- Explicitly models thermal inversions during the dry winter season (Dec--Feb) in CDMX and Toluca, trapping PM2.5 and Ozone.
- **Heavy Industry & Dust** -- Monterrey and northern border cities (Ciudad Juárez, Tijuana) are modeled with higher PM10 and PM2.5 baselines due to manufacturing, refineries, and arid environments.
- **Biomass Burning** -- Southern states (Chiapas, Oaxaca, Campeche, Quintana Roo) experience severe smoke spikes during the late dry season (Mar--May) due to agricultural fires and deforestation.
- **Missing Data Realism** -- Empty strings (NaN) randomly distributed throughout the pollutant columns to test data imputation strategies in MLOps pipelines.

---

## Dataset Specifications

| Property | Value |
|---|---|
| **File** | `mexico_air_quality_2014_2025.csv` |
| **Format** | CSV (UTF-8) |
| **Size** | ~1.8 MB |
| **Records** | 12,672 |
| **States/Entities** | 32 |
| **Cities** | 88 |
| **Date Range** | 2014-01-01 to 2025-12-01 |
| **Frequency** | Monthly |
| **Missing Values** | ~4.0% randomly distributed across pollutants |

---

## Column Dictionary

### Identifiers

| # | Column | Description | Type |
|---|---|---|---|
| 1 | `State` | State or Federal Entity name | String |
| 2 | `City` | City name | String |
| 3 | `Date` | Observation date (1st of each month) | Date (YYYY-MM-DD) |

### Air Pollutants (Includes Nulls)

| # | Column | Description | Unit | Type |
|---|---|---|---|---|
| 4 | `PM2.5 (ug/m3)` | Fine Particulate Matter <= 2.5 micrometers | ug/m3 | Float / Null |
| 5 | `PM10 (ug/m3)` | Particulate Matter <= 10 micrometers | ug/m3 | Float / Null |
| 6 | `NO (ug/m3)` | Nitric Oxide | ug/m3 | Float / Null |
| 7 | `NO2 (ug/m3)` | Nitrogen Dioxide | ug/m3 | Float / Null |
| 8 | `NOx (ppb)` | Total Nitrogen Oxides | ppb | Float / Null |
| 9 | `NH3 (ug/m3)` | Ammonia | ug/m3 | Float / Null |
| 10 | `CO (mg/m3)` | Carbon Monoxide | mg/m3 | Float / Null |
| 11 | `SO2 (ug/m3)` | Sulphur Dioxide | ug/m3 | Float / Null |
| 12 | `O3 (ug/m3)` | Ground-level Ozone | ug/m3 | Float / Null |
| 13 | `Benzene (ug/m3)` | Benzene (VOC) | ug/m3 | Float / Null |
| 14 | `Toluene (ug/m3)` | Toluene (VOC) | ug/m3 | Float / Null |
| 15 | `Xylene (ug/m3)` | Xylene (VOC) | ug/m3 | Float / Null |

### Air Quality Index

| # | Column | Description | Type |
|---|---|---|---|
| 16 | `AQI` | Air Quality Index (mapped using standard US EPA breakpoints) | Integer / Null |
| 17 | `AQI_Bucket` | Category: Good / Moderate / Unhealthy for Sensitive Groups / Unhealthy / Very Unhealthy / Hazardous | String / Null |

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

Based on SINAICA data and topographical challenges:

| Tier | Example Cities | PM2.5 Baseline (ug/m3) | Primary Driver |
|---|---|---|---|
| **High-Altitude Basin** | CDMX, Toluca, Puebla | 25--80 | Thermal inversions, massive vehicular traffic, high ozone due to altitude/sunlight. |
| **Heavy Industrial** | Monterrey, Saltillo, Torreón | 30--90 | Manufacturing, refineries, arid environment road dust. |
| **Dense Traffic** | Guadalajara, Tijuana, Ciudad Juárez | 20--60 | Heavy commuter and border-crossing traffic, light industry. |
| **Biomass / Deforestation** | Tuxtla Gutiérrez, Campeche | 10--35 | Relatively clean baselines but severe spikes during Mar-May fire season. |
| **Coastal / Clean** | Cancún, La Paz, Acapulco | 5--18 | Ocean breezes disperse pollutants rapidly; tourism-driven economies. |

---

## Seasonal and Temporal Patterns Modeled

| Season | Months | Effect | Explanation |
|---|---|---|---|
| **Thermal Inversions** | Dec -- Feb | PM2.5 Peak | Cold, dry winter months create thermal inversions in high-altitude basins (like CDMX), trapping pollutants near the surface. |
| **Biomass Burning** | Mar -- May | Smoke Peak | The late dry season sees a massive increase in agricultural fires and forest fires, particularly in the south. |
| **Pre-Monsoon / Heat** | Apr -- May | Ozone Peak | Intense sunlight and heat before the rains arrive catalyze the formation of ground-level ozone. |
| **Rainy Season** | Jun -- Oct | Washout | Heavy summer rains dramatically reduce airborne particulate matter, improving AQI across the country. |

---

## License and Citation

Released under **[Creative Commons CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**.
You are free to share and adapt this dataset for any purpose, provided you give appropriate credit and distribute contributions under the same license.

Please cite:

```
Mexico Air Quality Index Dataset (2014-2025)
32 Entities | 88 Cities | Monthly Observations (Jan 2014 -- Dec 2025)
Data modeled on published statistics from SINAICA, SEDEMA, IQAir, INEGI, and GFW.
```
