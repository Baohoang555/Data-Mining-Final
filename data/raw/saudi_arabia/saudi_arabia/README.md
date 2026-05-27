# Saudi Arabia Air Quality Dataset (2014-2025)

**Format:** CSV (UTF-8) | **Records:** 10800 | **License:** CC BY-SA 4.0

## About This Dataset
This dataset tracks the synthesized air quality of Saudi Arabia across 12 provinces and 75 key cities. It covers a twelve-year timeline (2014-2025), simulating the hyper-arid climatic conditions, extreme dust phenomena, and the massive emissions footprint of the global petrochemical and oil refining industries located throughout the Arabian Peninsula.

### Data Sources and Methodology

| Domain | Simulated Sources (Proxy Baselines) |
| ------------- |:-------------:|
| **Environmental Data** | [National Center for Environmental Compliance (NCEC KSA)](https://ncec.gov.sa/) |
| **Socio-Economic Data** | [World Bank Saudi Arabia Sector](https://data.worldbank.org/country/saudi-arabia) |
| **Emissions & Deforestation** | Copernicus Atmosphere Monitoring Service |

## Dataset Specifications
* Dataset rows: 10800
* Date Range: Jan 1, 2014 - Dec 1, 2025 (Monthly Data)
* Geography: 75 cities sampled regionally.
* Simulated Null Target: 0% continuous dataset as per request.

## Column Dictionary
Consists of the standard 23-column layout:
`State`, `City`, `Date`, `PM2.5 (ug/m3)`, `PM10 (ug/m3)`, `NO (ug/m3)`, `NO2 (ug/m3)`, `NOx (ppb)`, `NH3 (ug/m3)`, `CO (mg/m3)`, `SO2 (ug/m3)`, `O3 (ug/m3)`, `Benzene (ug/m3)`, `Toluene (ug/m3)`, `Xylene (ug/m3)`, `AQI`, `AQI_Bucket`, `Wind_Speed (km/h)`, `Humidity (%)`, `Deforestation_Rate_%`, `Industry_Growth_%`, `CO2_Emission_MT`, `Population_Density_per_SqKm`.

## Seasonal and Temporal Patterns Modeled
*   **Haboob & Shamal Winds (Dust Storms)**: Severe multi-multiplier PM10 spikes heavily populated across Spring and Summer months (March-August).
*   **Extreme Petrochemical SO2/VOCs**: World-leading industrial baseline signatures targeting Jubail, Yanbu, Dhahran, and Ras Tanura.
*   **Summer Peak Power Loads**: Heightened NO2, SO2, and CO2 emissions tracking maximum air conditioning / desalination load from June-September.
*   **Arid Geography**: Exceptionally low humidity across interior provinces (Riyadh, Qassim) alongside almost zero agricultural ammonia and nil deforestation rates.

## AQI Reference 
Uses standard US EPA breakpoints based on PM2.5 concentrations.
