# Ethiopia Air Quality Index (AQI) Dataset (2014-2025)

**Format:** CSV (UTF-8)
**Records:** 10,224
**License:** CC BY-SA 4.0

---

## About This Dataset

A comprehensive, research-backed Air Quality dataset covering **all 12 Regional States and 2 Chartered Cities of Ethiopia** with **71 major cities** across a **12-year span (Jan 2014 -- Dec 2025)**.

Ethiopia's air quality profile is distinct from heavily industrialized nations. While its per capita CO2 emissions are among the lowest globally, major urban centers like Addis Ababa suffer from severe particulate matter (PM2.5) pollution driven by an aging vehicle fleet, unpaved roads, rapid construction, and widespread reliance on biomass fuels (wood/charcoal) for cooking and heating. This dataset accurately models these anthropogenic sources alongside natural phenomena like the seasonal dust storms in the arid eastern regions (Afar, Somali).

> **Note on Real-World Missing Data Simulation**: Per user specification, this dataset intentionally includes approximately **~4.0% missing values (nulls)** for pollutant columns. This accurately simulates real-world sensor downtime and data gaps common in developing national monitoring networks.

### Data Sources and Methodology

Due to limited centralized continuous air quality monitoring across all regions, this dataset synthesizes pollution patterns, baselines, and seasonal dynamics from the following verified sources:

| Source | Link | Usage |
|---|---|---|
| **UNEP / EPA Ethiopia** | [unep.org/regions/africa](https://www.unep.org/regions/africa) | Environmental Protection Authority reports on urban air quality challenges |
| **IQAir** | [iqair.com/ethiopia](https://www.iqair.com/ethiopia) | Historical PM2.5 baselines for Addis Ababa and localized sensor networks |
| **World Bank Data** | [data.worldbank.org](https://data.worldbank.org/indicator/EN.ATM.PM25.MC.M3?locations=ET) | Annual PM2.5 exposure estimates, population density, and exceptionally low CO2 baselines |
| **Global Forest Watch** | [globalforestwatch.org](https://www.globalforestwatch.org/dashboards/country/ETH/) | Deforestation rates and tree cover loss, primarily impacting southern and western regions |

### Key Features

- **Geographic coverage:** All 12 Regional States (Afar, Amhara, Benishangul-Gumuz, Central Ethiopia, Gambela, Harari, Oromia, Sidama, Somali, South Ethiopia, Southwest Ethiopia, Tigray) and 2 Chartered Cities (Addis Ababa, Dire Dawa).
- **Monthly granularity:** 144 months (Jan 2014 -- Dec 2025).
- **23 columns:** Pollutants, meteorological, socio-economic, and environmental indicators.
- **Addis Ababa Mega-City Effect:** Explicitly models severe PM2.5 and NOx spikes in the capital due to traffic congestion and biomass burning.
- **Arid Dust Storms:** Models extreme PM10 (coarse particulate matter) spikes during the dry season (Feb-May) in the Afar and Somali regions.
- **Kiremt Washout:** Simulates the dramatic improvement in air quality during the main rainy season (June-September).
- **Missing Data Realism:** Empty strings (NaN) randomly distributed throughout the pollutant columns to test data imputation strategies in MLOps pipelines.

---

## Dataset Specifications

- **File:** `ethiopia_air_quality_2014_2025.csv`
- **Format:** CSV (UTF-8)
- **Size:** ~1.4 MB
- **Records:** 10,224
- **Regions/Entities:** 14
- **Cities:** 71
- **Date Range:** 2014-01-01 to 2025-12-01
- **Frequency:** Monthly
- **Missing Values:** ~4.0% randomly distributed across pollutants

---

## Column Dictionary

### Identifiers

1. `Region`: Regional State or Chartered City name
2. `City`: City name
3. `Date`: Observation date (1st of each month)

### Air Pollutants (Includes Nulls)

4. `PM2.5 (ug/m3)`: Fine Particulate Matter
5. `PM10 (ug/m3)`: Particulate Matter
6. `NO (ug/m3)`: Nitric Oxide
7. `NO2 (ug/m3)`: Nitrogen Dioxide
8. `NOx (ppb)`: Total Nitrogen Oxides
9. `NH3 (ug/m3)`: Ammonia
10. `CO (mg/m3)`: Carbon Monoxide
11. `SO2 (ug/m3)`: Sulphur Dioxide
12. `O3 (ug/m3)`: Ground-level Ozone
13. `Benzene (ug/m3)`: Benzene (VOC)
14. `Toluene (ug/m3)`: Toluene (VOC)
15. `Xylene (ug/m3)`: Xylene (VOC)

### Air Quality Index

16. `AQI`: Air Quality Index (US EPA breakpoints)
17. `AQI_Bucket`: Category (Good / Moderate / Unhealthy for Sensitive Groups / Unhealthy / Very Unhealthy / Hazardous)

### Meteorological Parameters

18. `Wind_Speed (km/h)`: Average wind speed
19. `Humidity (%)`: Relative humidity

### Socio-Environmental Indicators

20. `Deforestation_Rate_%`: Annual deforestation/tree cover loss rate
21. `Industry_Growth_%`: Industrial output year-over-year growth
22. `CO2_Emission_MT`: Region-level CO2 emissions (Extremely low baseline)
23. `Population_Density_per_SqKm`: People per square kilometer

---

## Pollution Tier Classification

| Tier                    | Example Cities                | PM2.5 Baseline (ug/m3) | Primary Driver                                                            |
| ----------------------- | ----------------------------- | ---------------------- | ------------------------------------------------------------------------- |
| **Mega-City**     | Addis Ababa                   | 35--120                | Heavy traffic (old fleet), intense biomass fuel usage, construction dust. |
| **Urban Hub**     | Dire Dawa, Bahir Dar, Hawassa | 20--65                 | Medium traffic, municipal waste burning, localized biomass burning.       |
| **Arid / Dust**   | Jijiga, Semera                | 15--45                 | Extreme PM10 from natural desert dust storms; low anthropogenic PM2.5.    |
| **Moderate**      | Harar, Debre Markos           | 10--35                 | Mixed light urban activity.                                               |
| **Rural / Green** | Bonga, Asosa                  | 5--20                  | Vast uninhabited forests/savannas; extremely clean baseline air.          |

---

## Seasonal and Temporal Patterns Modeled

| Season                        | Months     | Effect       | Explanation                                                                                                              |
| ----------------------------- | ---------- | ------------ | ------------------------------------------------------------------------------------------------------------------------ |
| **Dry Season (Bega)**   | Oct -- Jan | Biomass Peak | Cold nights drive high biomass (wood/charcoal) burning for heating/cooking, trapping PM near the ground.                 |
| **Short Rains / Dust**  | Feb -- May | PM10 Peak    | High winds in arid eastern regions (Afar/Somali) trigger massive dust storms.                                            |
| **Long Rains (Kiremt)** | Jun -- Sep | Washout      | Sustained, heavy rainfall washes out nearly all airborne particulate matter, bringing AQI to "Good" across most regions. |

---

## License and Citation

Released under **[Creative Commons CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**.
You are free to share and adapt this dataset for any purpose, provided you give appropriate credit and distribute contributions under the same license.

Please cite:

```
Ethiopia Air Quality Index Dataset (2014-2025)
14 Regions/Entities | 71 Cities | Monthly Observations (Jan 2014 -- Dec 2025)
Data modeled on published statistics from UNEP, World Bank, IQAir, and GFW.
```
