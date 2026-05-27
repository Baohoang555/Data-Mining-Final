# Philippines Air Quality Dataset (2014-2025)

**Format:** CSV (UTF-8) | **Records:** 15408 | **License:** CC BY-SA 4.0

## About This Dataset
This dataset tracks the air quality of the Philippines across 17 major administrative regions and over 100 cities. It covers a twelve-year timeline (2014-2025), synthesizing localized pollution metrics alongside socio-economic indicators and distinct geographical/climatic seasons.

### Data Sources and Methodology

| Domain | Simulated Sources (Proxy Baselines) |
| ------------- |:-------------:|
| **Air Quality Guidelines** | [WHO Air Quality](https://www.who.int/health-topics/air-pollution) & Philippine DENR |
| **Socio-Economic Data** | [World Bank Philippines Sector](https://data.worldbank.org/country/philippines) |
| **Emissions & Deforestation** | [Global Forest Watch](https://www.globalforestwatch.org/dashboards/country/PHL) |
| **Weather & Seasonal** | [PAGASA](http://bagong.pagasa.dost.gov.ph/) |

### Key Features
* **Detailed Regional Coverage**: Data spans from Northern Luzon (Cordillera) to BARMM in Mindanao.
* **Realistic Weather & Monsoon Patterns**: Simulated with wet season (Habagat) multipliers to wash out PM levels and dry seasons (Amihan) where heat/biomass burnoffs elevate particulates.
* **Tier-based Spatial Density**: Metropolitan areas (NCR) are modeled with high emissions, while provincial regions simulate lower baseline pollution, aligning with actual industry footprints.

## Dataset Specifications
* Dataset rows: 15,408
* Date Range: Jan 1, 2014 - Dec 1, 2025 (Monthly Data)
* Geography: 107 cities across 17 regions.
* Simulated Null Target: ~4% missing values on sensor pollutant limits to emulate real downtime events.

## Column Dictionary
Consists of the standard 23-column layout:
`State`, `City`, `Date`, `PM2.5 (ug/m3)`, `PM10 (ug/m3)`, `NO (ug/m3)`, `NO2 (ug/m3)`, `NOx (ppb)`, `NH3 (ug/m3)`, `CO (mg/m3)`, `SO2 (ug/m3)`, `O3 (ug/m3)`, `Benzene (ug/m3)`, `Toluene (ug/m3)`, `Xylene (ug/m3)`, `AQI`, `AQI_Bucket`, `Wind_Speed (km/h)`, `Humidity (%)`, `Deforestation_Rate_%`, `Industry_Growth_%`, `CO2_Emission_MT`, `Population_Density_per_SqKm`.

## Philippines Administrative Level Coverage
- NCR (National Capital Region)
- Cordillera Administrative Region (CAR)
- Regions I to XIII
- BARMM (Bangsamoro Autonomous Region in Muslim Mindanao)

## Pollution Tier Classification
*   **Mega-City / Primary Urban Hub**: (e.g., NCR Cities, Metro Cebu, Metro Davao) Modest to heavy industrial output, intense vehicular traffic.
*   **Regional Economic Hub**: (e.g., CALABARZON cities, Central Luzon). Dense populations with growing economic zones.
*   **Provincial / Coastal**: General provincial cities across Visayas and Mindanao with clean trade-winds, lower industrial density.

## Seasonal and Temporal Patterns Modeled
*   **Monsoon (Wet Season)** Multipliers to emulate rain washing out particulate matter (June - October).
*   **Hot Dry Season** Adjusting for heightened humidity (March - May) and related pollution stagnation.

## Suggested Use Cases
*   Spatio-temporal analysis of archipelago and coastal city pollution vs. dense mega-city pollution. 
*   Predicting impact of rapid urbanization on adjacent provinces (like CALABARZON).
*   Evaluating policy interventions on air quality based on the Philippine Clean Air Act.

## AQI Reference 
Uses standard US EPA breakpoints based on PM2.5 concentrations.

## License and Citation
Licensed under Creative Commons CC BY-SA 4.0. Please cite this artificial dataset responsibly if used in external reporting dashboards.
