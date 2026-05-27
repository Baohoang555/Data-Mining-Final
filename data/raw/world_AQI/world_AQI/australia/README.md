# Australia Air Quality Dataset (2014-2025)

**Format:** CSV (UTF-8) | **Records:** 10512 | **License:** CC BY-SA 4.0

## About This Dataset
This dataset tracks the synthesized air quality of Australia across all 8 states/territories, mapping out 75 cities from Sydney to Perth. It covers a twelve-year timeline (2014-2025), simulating significant localized pollution dynamics mapped directly to geographical layout, population distributions, and unique environmental phenomena like severe summer bushfires.

### Data Sources and Methodology

| Domain | Simulated Sources (Proxy Baselines) |
| ------------- |:-------------:|
| **Environmental Data** | [Department of Climate Change, Energy, the Environment and Water (DCCEEW)](https://www.dcceew.gov.au/) |
| **Socio-Economic Data** | [World Bank Australia Sector](https://data.worldbank.org/country/australia) |
| **Emissions & Deforestation** | Copernicus Atmosphere Monitoring Service |

## Dataset Specifications
* Dataset rows: 10512
* Date Range: Jan 1, 2014 - Dec 1, 2025 (Monthly Data)
* Geography: 75 cities sampled regionally.
* Simulated Null Target: 0% continuous dataset as per request.

## Column Dictionary
Consists of the standard 23-column layout:
`State`, `City`, `Date`, `PM2.5 (ug/m3)`, `PM10 (ug/m3)`, `NO (ug/m3)`, `NO2 (ug/m3)`, `NOx (ppb)`, `NH3 (ug/m3)`, `CO (mg/m3)`, `SO2 (ug/m3)`, `O3 (ug/m3)`, `Benzene (ug/m3)`, `Toluene (ug/m3)`, `Xylene (ug/m3)`, `AQI`, `AQI_Bucket`, `Wind_Speed (km/h)`, `Humidity (%)`, `Deforestation_Rate_%`, `Industry_Growth_%`, `CO2_Emission_MT`, `Population_Density_per_SqKm`.

## Seasonal and Temporal Patterns Modeled
*   Adjusted specifically to Australia's prevalent weather patterns such as devastating summer bushfire seasons that drastically elevate PM2.5 across continents.

## AQI Reference 
Uses standard US EPA breakpoints based on PM2.5 concentrations.
