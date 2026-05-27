# Egypt Air Quality Dataset (2014-2025)

**Format:** CSV (UTF-8) | **Records:** 10800 | **License:** CC BY-SA 4.0

## About This Dataset
This dataset tracks the synthesized air quality of Egypt across 25 major governorates and regions mapping out 75 cities. It covers a twelve-year timeline (2014-2025), simulating significant pollution events such as the Khamsin sandstorms and the Black Cloud phenomenon found in the Nile Delta.

### Data Sources and Methodology

| Domain | Simulated Sources (Proxy Baselines) |
| ------------- |:-------------:|
| **Air Quality Guidelines** | [Egyptian Environmental Affairs Agency (EEAA)](https://www.eeaa.gov.eg/) & WHO |
| **Socio-Economic Data** | [World Bank Egypt Sector](https://data.worldbank.org/country/egypt-arab-rep) |
| **Emissions & Deforestation** | Copernicus Atmosphere Monitoring Service |
| **Weather & Seasonal** | Egyptian Meteorological Authority |

### Key Features
* **Detailed Regional Coverage**: Data spans densely populated Nile Delta agriculture, massive urbanization in Cairo, down to the arid Western Desert. 
* **Realistic Weather & Seasonal Patterns**: Simulated with the "Khamsin" (March - May) causing severe PM10 spikes, and the "Black Cloud" in Autumn (Oct - Nov) driving PM2.5 up due to biomass burning.
* **Tier-based Spatial Density**: Metropolitan areas (Greater Cairo) and industrial hubs are modeled with high emissions, while desert and coastal cities (Red Sea, Matrouh) simulate much lower baseline pollutions.

## Dataset Specifications
* Dataset rows: 10,800
* Date Range: Jan 1, 2014 - Dec 1, 2025 (Monthly Data)
* Geography: 75 cities across 25 governorates.
* Simulated Null Target: 0% (Clean continuous dataset as per request).

## Column Dictionary
Consists of the standard 23-column layout:
`State`, `City`, `Date`, `PM2.5 (ug/m3)`, `PM10 (ug/m3)`, `NO (ug/m3)`, `NO2 (ug/m3)`, `NOx (ppb)`, `NH3 (ug/m3)`, `CO (mg/m3)`, `SO2 (ug/m3)`, `O3 (ug/m3)`, `Benzene (ug/m3)`, `Toluene (ug/m3)`, `Xylene (ug/m3)`, `AQI`, `AQI_Bucket`, `Wind_Speed (km/h)`, `Humidity (%)`, `Deforestation_Rate_%`, `Industry_Growth_%`, `CO2_Emission_MT`, `Population_Density_per_SqKm`.

## Egypt Governorates Coverage
- Greater Cairo (Cairo, Giza, Qalyubia)
- Nile Delta (Dakahlia, Sharkia, Gharbia, Beheira, Monufia, Kafr El Sheikh, Damietta)
- Suez Canal Zone (Port Said, Ismailia, Suez)
- Alexandria & North Coast
- Western Desert (New Valley, Matrouh)
- Upper Egypt (Faiyum, Beni Suef, Minya, Asyut, Sohag, Qena, Luxor, Aswan)
- Sinai & Red Sea

## Pollution Tier Classification
*   **Mega-City / Primary Urban Hub**: (e.g., Cairo, Alexandria). Modest to heavy industrial output, intense vehicular traffic.
*   **Industrial Hub**: (e.g., 10th of Ramadan, Sadat City, Suez). High emissions of NO2, SO2, and particulates.
*   **Nile Delta (Agricultural)**: Severe seasonal PM2.5 spikes due to agricultural burning (Black Cloud).
*   **Coastal & Desert**: (e.g., Sharm El Sheikh, Hurghada, Kharga). Clean baseline winds but prone to massive PM10 spikes from dust storms.

## Seasonal and Temporal Patterns Modeled
*   **Khamsin Wind (Spring)**: Severe Saharan dust storms drastically blowing up PM10 measurements globally (March - May).
*   **Black Cloud (Autumn)**: Acute PM2.5 pollution in Cairo and the Delta due from burning rice straw (October - November).

## Suggested Use Cases
*   Spatio-temporal analysis of agricultural burning vs urban emission contributions. 
*   Analyzing the particulate differential between coarse dust (PM10) in deserts and fine particulates (PM2.5) in traffic-jammed mega-cities.

## AQI Reference 
Uses standard US EPA breakpoints based on PM2.5 concentrations.

## License and Citation
Licensed under Creative Commons CC BY-SA 4.0. Please cite this artificial dataset responsibly if used in external reporting dashboards.
